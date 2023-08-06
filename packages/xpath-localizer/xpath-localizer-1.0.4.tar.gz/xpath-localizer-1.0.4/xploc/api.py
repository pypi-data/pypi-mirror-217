#!/usr/bin/env python3
import sys
import os
import re
import codecs

from xploc import util
from xploc import loader

#
#   XPath selectors: https://www.w3schools.com/xml/xpath_syntax.asp
#   Playwirght selectors: https://playwright.dev/docs/selectors#text-selector
#

def traverse_tree(rootdir,locale="en",filetype="properties",verbose=False,ignore_path_list=None):
    basefiles = util.get_basefiles(rootdir,filetype=filetype,verbose=verbose,ignore_path_list=ignore_path_list)

    properties = {}

    for file in basefiles:
        p = loader.load_files(basefiles[file]["en"],verbose=verbose)
        if locale != "en":
            lfile = util.locale_lookup(basefiles[file]["en"],locale)
            if lfile and lfile != basefiles[file]["en"]:
                l = loader.load_files(lfile)
                p.update(l)
            else:
                if lfile:
                    relpath = os.path.relpath(lfile)
                    if verbose:
                        print (f'Warning: properties file "{relpath}" is not localized for the target locale "{locale}".')
                else:
                    if verbose:
                        print (f'Warning: file "{file}" is not recognized for the locale "{locale}".')

        properties.update(p)

    return properties

value_pat = re.compile(r'(?<=\s\s)(?P<value>\S.*)(?=\s\s)')
value2_pat = re.compile(r'(?<=\s\s)(?P<value>\S.*)')
I18NOK_pat = re.compile(r"#\s*i18n:OK")
comment_pat = re.compile(r"\s*#.*|\*\*\*")
placeholder_pat = re.compile(r'\(_+\w+_+\)')

def extract(path,variables=None,verbose=False,all_variables=None,playwright=False):
    propfile = ""
    robotfile = ""
    syspropfile = ""
    sysprop = []

    if not os.path.exists(path):
        print (f"{path} does not exist.")
        return None, None, None

    with codecs.open(path,'r',encoding='utf-8') as fp:
        lines = fp.readlines()

    keys = {}  # store new keys
    variable_section = False
    for line in lines:

        #
        ## handle control statements
        #
        if line.startswith("*** Variables ***"):
            variable_section = True
        elif line.startswith("*** Keywords ***") or line.startswith("*** Settings ***"):
            variable_section = False
        m = comment_pat.match(line)
        if not m:
            m = I18NOK_pat.search(line)
        if m or not variable_section or line=="\n" or line == "\r\n" or is_selector_class(line):
            robotfile += line  # just copy line
            continue

        def update_props_vars(props,vars):
            propfile = ""
            if len(props) > 0:
                sysprop.extend(props)  # append it
            for var in vars:
                if var["key"] not in keys:
                    propfile += f"{var['key']} = {var['value']}\n"
                    keys[var['key']] = 0
                keys[var['key']] += 1
            return propfile

        if playwright and is_selector_pw(line):
            found, line, props, vars = extract_selector_pw(line,variables,all_variables,verbose=verbose)
            if found:
                robotfile += line
                propfile += update_props_vars(props,vars)
                continue

        ## xpath: or playwright xpath: or xpath=
        if is_selector_xpath(line):
            found, line, props , vars = extract_selector_xpath(line,variables,all_variables,verbose=verbose)
            if found:
                robotfile += line
                propfile += update_props_vars(props,vars)
                continue

        # is_var_value should be checked lastly to avoid wrong-detection.
        print(f"before var_value={line}")
        if is_var_value(line):
            found, line, props , vars = extract_var_value(line,variables,verbose=verbose)
            if found:
                robotfile += line
                propfile += update_props_vars(props,vars)
                continue
        else:
            print (f"Unknown statement: '{line}'")

        robotfile += line
        # end of line loop

    return robotfile, propfile, sysprop

def is_selector_pw(line):
    n = pwprop_pat.search(line)
    if n:
        return True
    return False

pw_hastext_pat = re.compile(r'''(?P<cclass>:has-text|:text)\((['"])(?P<T>.*?)\2\)''')
pw_textq_pat = re.compile(r'''(?P<cclass>text)\s*=\s*(['"])(?P<T>.*?)\2''')
pw_text_pat = re.compile(r'''(?P<cclass>text)\s*=\s*(?P<T>.*?)$''')
def extract_selector_pw(line,variables,all_variables,verbose=None):
    # playwright text selectors
    #   text="Log in", :has-text("Log in"), text='Login', text=Log in , "Log in" , 'text=/Log\\s*in/i', :text("Log in")
    #   aria-label="text", aria-label='text'
    #   placeholder="text", placeholder='text'
    # "|" operator can be used to combine multiple translations
    # "," operator can be used to combine multiple translations in css selector
    # test file: ui-projects/resources/common/library/visualization_common_locators.robot
    props = []
    vars = []
    in_paren = False

    m = pw_pat.search(line)
    if not m:
        # result special pattern here
        m = pw_text_pat.search(line)
        if not m:
            m = pw_textq_pat.search(line)
        if not m:
            m = pw_hastext_pat.search(line)
            in_paren = True
        if m:
            value = m.group('T')
            cclass = m.group('cclass')
            if is_placeholder(value):
                return True, line, [], []  # placeholder only
            print(f"selector_pw: {cclass} : '{value}'")
            var = varname(value)
            if variables:
                props.extend(bundle_reference(value,variables))
                print (f"{props}")

            value0 , nhit = var_reference(value,variables,hint="label",verbose=verbose)
            if nhit:
                if in_paren:
                    line = line[:m.start()] + cclass + '("' + '${' + value0 + '}' + '")' +  line[m.end():]
                else:
                    line = line[:m.start()] + cclass + '="' + '${' + value0 + '}' + '"' +  line[m.end():]
            else:
                if in_paren:
                    line = line[:m.start()] + cclass + '("' + '${' + var + '}' + '")' + line[m.end():]
                else:
                    line = line[:m.start()] + cclass + '="' + '${' + var + '}' + '"' + line[m.end():]
                vars.append({ "key":var , "value":value })
            return True, line, props, vars

        n = pw_hastext_pat.search(line)
        if n:
            value = n.group('T')
            print(f"Unresolved pwvalue: {line}")
    else:
        # print (f"Warning: should be handled in extract_selector_xpath: {line}")
        pass

    return False, line, props, vars

def is_var_value(line):
    m = value_pat.search(line)
    if not m:
        m = value2_pat.search(line)
    if m:
        value = m.group('value')
        if not value.startswith('xpath') and not value.startswith('class:'):
            return True
    return False

def extract_var_value(line,variables,verbose=False):
    m = value_pat.search(line)
    if not m:
        m = value2_pat.search(line)
    if m:
        value = m.group('value')
    else:
        return False, None, None, None

    # remove comments? here?
    if value.find('  #'):
        value = value.replace('  #','\n')
        value = value.split('\n')[0]
    value = value.strip()

    # check whether value is localizable
    if is_non_localizable(value):
        return False, line, [], []

    # process variables
    var = varname(value)
    if variables:
        props = bundle_reference(value,variables)
    else:
        props = []

    #
    # robot variable reference does not support multiple translations.
    #   It will always use a simple assingment to redirect to property reference.
    #
    value , nhit = var_reference(value,variables,hint="label",verbose=verbose)
    if nhit:
        # print (f"var={var} value={value} {m.start()} {m.end()}")
        line = line[:m.start()] + "${" + value + "}" + line[m.end():]
        vars = []
    else:
        line = line[:m.start()] + "${" + var + "}" + line[m.end():]
        vars =  [{ "key":var , "value":value }]

    return True, line, props, vars

class_pat = re.compile(r'(?<=\s\s)(?P<value>class:\S.*)')
def is_selector_class(line):
    m = class_pat.search(line)
    if m:
        print (f"Debug - class found: {line}")
        return True
    return False

def is_selector_xpath(line):
    m = value_pat.search(line)
    if not m:
        m = value2_pat.search(line)
    if not m:
        return False
    value = m.group('value')
    if value.startswith('xpath') or value.startswith('//*') or value.startswith('css:'):
        return True
    m = pwprop_pat.match(value)
    if m:
        return True
    return False

def is_non_localizable(value):
    if " " in value:
        return False
    for ngchar in "_-":
        if ngchar in value:
            return True
    return False

#text_pat = re.compile(r'''(?P<cclass>text\(\)\s*|@aria-label\s*|@placeholder\s*|@title\s*|\.\s*?)(?P<dlm>[=,]\s*)(['"])(?P<T>.*?)\3''')
#text_pat = re.compile(r'''(?P<oper>contains\s*\(\s*)?(?P<cclass>text\(\)\s*|@aria-label\s*|@placeholder\s*|@title\s*|\.\s*?)(?P<dlm>[=,]\s*)(['"])(?P<T>.*?)\4(?P<oper_end>\s*\))?''')
# (?P<oper>contains\s*\(\s*)?
# (?P<oper>\(\s*)?
#text_pat = re.compile(r'''(?P<oper>contains\s*\(\s*)?(?P<cclass>text\(\)\s*|@aria-label\s*|@placeholder\s*|@title\s*|\.\s*?)(?P<dlm>[=,]\s*)(['"])(?P<T>.*?)\4(?P<oper_end>\s*\))?''')
text_pat = re.compile(r'''(?P<oper>(contains|starts-with)\s*\(\s*)?(?P<cclass>text\(\)\s*|@aria-label\s*|@placeholder\s*|@title\s*|\.\s*?)(?P<dlm>[=,]\s*)(['"])(?P<T>.*?)\5(?P<oper_end>\s*\))?''')
pw_pat = re.compile(r'''(?P<oper>\[\s*\(?\s*)?(?P<cclass>text\s*|aria-label\s*|placeholder\s*|@title\s*|\.\s*?)(?P<dlm>[=]\s*)(['"])(?P<T>.*?)\4(?P<oper_end>\s*\)?\s*\])?''')
pwprop_pat = re.compile(r'''\[(id|aria-label|placeholder|text)\s*=.*\]|text\s*=|css\s*=|:has-text\s*\(''')
def extract_selector_xpath(line,variables, all_variables, verbose=None, locale=None, add_english=False,fuzzy_match=False):
    langlist = None
    if locale:
        langlist = []
        langlist.append(locale)
    m = pwprop_pat.search(line)  # is playwright selector
    if m:
        seg = pw_pat.finditer(line)   # playwright xpath
    else:
        seg = text_pat.finditer(line)  # robot xpath

    if seg:
        count = 0
        lastchar = 0
        props = [] # initialize per line
        vars = []
        edlist = []
        for m in iter(seg):
            prop = []  # initialize props per value
            strcls = m.group('cclass')
            #print (f"strcls={strcls}")
            value = m.group('T')
            var = varname(value)
            if is_placeholder(value):  # value only contains a placeholder
                continue

            #newline = newline[:m.start()] + m.group(1) + m.group(2) + "'" + var + "'" + newline[m.end():]
            if variables:
                prop = bundle_reference(value,variables)
                props.extend(prop)

            value0 , nhit = var_reference(value,variables,hint=strcls,verbose=verbose)
            if nhit:
                #print (f"Indirect reference: {var} = {value}")
                var = value0
                # if fuzzy_match:
                #     print (f"var_reference: var={var} value0={value0} nhit={nhit}")
            elif fuzzy_match:
                value0, nhit = var_fuzzy_match(value,variables,verbose=verbose)
                if nhit:
                    # print (f"var_fuzzy_match: var={var} value0={value0} nhit={nhit}")
                    nhit = 0  # reset nhit not to call detect_varint_trans
                    #var = value0
                    var = value0 + "*"  # append "* to indicate fuzzy matching
                else:
                    vars.append({ "key":var, "value":value })  # unresolved in fuzzy match
            else:
                vars.append({ "key":var, "value":value })

            varlist = None
            if all_variables and nhit:
                #print(f"Debug0: nhit={nhit} {varlist} {var} props={props}")
                varlist = detect_variant_trans(var,prop,all_variables,hint=strcls,langlist=langlist)

            edlist.append({"begin":m.start(), "end":m.end(),"var":var if not varlist else varlist,
                "g1":m.group('cclass'), "g2":m.group('dlm'),
                "oper":m.group('oper'), "oper_end":m.group('oper_end'), "value":value})
            count += 1

        if count == 0:
            return True, line, props, vars   #return True and discad untranslatable patterns

        edlist.reverse()
        if locale:
            line = edit_line(line,edlist,all_variables,new_variables=vars,locale=locale,add_english=add_english)
            # resolve variables for locale
        else:
            line = edit_line(line,edlist)

    else:
        print (f"Return from finditer is None: {line}")
        return False, line, [], []

    return True, line, props, vars

def varname(label):
    label = label.strip()
    label = label.lower().replace(' ','_')
    label = label.replace(':','C')
    label = label.replace('?','Q')
    label = label.replace('.','P')
    label = label.replace(',','M')
    label = label.replace('"','D')
    label = label.replace('{','L')
    label = label.replace('}','R')
    label = label.replace('(','S')
    label = label.replace(')','T')
    label = label.replace('$','V')
    label = label.replace("'",'A')
    label = label.replace("[",'B')
    label = label.replace("]",'E')
    label = label.replace("\\",'F')
    label = label.replace("-",'U')
    label = label.replace("®",'G')
    #label = "${" + label +  "}"
    return label

def var_reference(label,variables=None,hint=None,verbose=False):
    # hint: text(), ., @placeholder, @aria-label, @title
    # title does not mean <title>, but title= attribute.
    chrclass = { "placeholder":[], "label":[], "title":[], "tooltip":[], "icon":[], "prefix":[] }
    nhit = 0
    candidates = []

    #
    debug = False

    if not variables:
        return label, 0

    for key in variables:
        if variables[key] == label:
            nhit += 1
            candidates.append(key)

    if debug:
        print (f"label={label} {candidates}")
    if len(candidates)==0:
        return label, 0
    if len(candidates)==1:  # only one found
        label = candidates[0]
        return label, 1

    # if multiple hit
    if verbose:
        print(f"candidates={candidates}")

    # clasify keys
    for key in candidates:
        lkey = key.lower()
        if lkey.find("icon")>=0:
            chrclass["icon"].append(key)
        elif lkey.find("title")>=0:
            chrclass["title"].append(key)
        elif lkey.find("placeholder")>=0:
            chrclass["placeholder"].append(key)
        elif lkey.find("label")>=0:
            chrclass["label"].append(key)
        elif lkey.find("tooltip")>=0:
            chrclass["tooltip"].append(key)
        elif lkey.find("prefix")>=0:
            chrclass["prefix"].append(key)
        else:
            chrclass["label"].append(key)

    def select(key,list):
        ncount = len(chrclass[key])
        if ncount >=1:
            if ncount >1 and verbose:
                print (f'Warning: {ncount} keys found for {key}:')
                for st in chrclass[key]:
                    print (f"\t{st}")
            return chrclass[key][0], ncount
        return None, ncount
    if debug:
        print(f"{chrclass}")
    if hint == "@title":
        # try icon first, then title
        label0, count0 = select("title",candidates)
        if count0 > 0:
            return label0, count0
    elif hint == "@placeholder":
        label0, count0 = select("placeholder",candidates)
        if count0 > 0:
            return label0, count0
    elif hint == "@aria-label":
        label0, count0 = select("label",candidates)
        if count0 > 0:
            return label0, count0
    elif hint == "prefix":
        label0, count0 = select("prefix",candidates)
        if count0 > 0:
            return label0, count0

    label0, count0 = select("label",candidates)
    if count0 > 0:
        return label0, count0

    # text() or .
    label0 , count0 = select("title",candidates)
    if count0 >0:
        return label0, count0

    label = candidates[0]
    nhit = len(candidates)
    if verbose:
        print (f'Warning: {nhit} keys found for text():')
        for st in candidates:
            print (f"\t{st}")

    return candidates[0], nhit

def bundle_reference(label,variables):
    candidates = []
    for key in variables:
        if variables[key] == label:
            candidates.append(key)
    return candidates

def generate_bundle(keys,variables=None):
    propfile = ""
    added_keys = {}
    if not variables:
        return propfile
    for key in keys:
        if key in added_keys:
            # print(f"duplicated entries {key}")
            added_keys[key] += 1
            continue
        added_keys[key] = 1
        propfile += f"{key} = {variables[key]}\n"
    return propfile

def write_file(path,buffer,destname):
    dir = os.path.dirname(path)
    if dir and not os.path.exists(dir):
        sys.stderr.write(f"Error: directory {dir} does not exist\n")
        return 0
    with codecs.open(path,'w','utf-8') as outp:
        outp.write(buffer)
    nlines = buffer.count('\n')
    #print (f"{destname} written to \"{path}. {nlines}")
    print (f"{nlines} lines written to \"{path}\".")
    return 1

def detect_variant_trans(def_key,props,all_variables,hint=None,langlist=None):
    # return list of variables if variant translation found
    #print(f"Debug: def_key={def_key} props={props} ")
    if not all_variables:
        return None
    count = 0
    uniq_keys = []
    uniq_trans = {}

    uniq_keys.append(def_key)
    english_string = all_variables["variables"]['en'][def_key]
    uniq_trans[english_string] = 1   # register EN string
    props.insert(0,def_key)

    for key in props:
        for loc in all_variables["locales"]:
            if langlist and loc not in langlist:
                continue  # skipt language
            if all_variables["variables"][loc][key] not in uniq_trans:
                uniq_trans[all_variables["variables"][loc][key]] = 0
                if key not in uniq_keys:
                    uniq_keys.append(key)

                uniq_trans[all_variables["variables"][loc][key]] += 1
    count = len(uniq_keys)
    if count>1:
        print(f"variants found: ={uniq_keys}")
        print(f"\t{uniq_trans}")
        return uniq_keys
    return None

def edit_line(line,edlist,all_variables=None,new_variables=None,locale=None,add_english=False):
    # print (f"Debug(edlilne):\t{line}\n\t{edlist}")
    newline = line
    variables = []
    loc_variables = []
    new = {}
    if all_variables and locale:
        variables = all_variables["variables"]["en"]
        loc_variables = all_variables["variables"][locale]
    if new_variables:
        for va in new_variables:
            new[va["key"]] = va["value"]

    def resolve_var(var,value,variables,loc_variables):
        if variables:
            if var.endswith("*"): # fuzzy matching
                resolved = resolve_fuzzy_variable(var,value,variables,loc_variables)
                var = '"' + resolved + '"'
                return var

            if var in loc_variables:
                var = '"' + loc_variables[var] + '"'
            elif var in variables:
                var = '"' + variables[var] + '"'
            elif new and var in new:
                var = '"' + new[var] + '"'
            else:
                print (f"Warning: Unresolved variable: {var}")
                var = '"${' + var + '}"'
        else:
            var = '"${' + var + '}"'
        return var

    for edstr in edlist:
    #newline = newline[:ix["begin"]] + ix["g1"] + ix["g2"] + '"${' + ix["var"] + '}"' + newline[ix["end"]:]
    #line = edit_line(line,ix)

        outer_op = ""
        outer_cl = ""
        openstr = ""
        closestr = ""
        if edstr["oper"] and edstr['oper_end']:
            openstr = edstr["oper"]
            closestr = edstr["oper_end"]
        elif edstr["oper"]:
            outer_op = edstr["oper"]
        elif edstr["oper_end"]:
            outer_cl = edstr["oper_end"]
        value = edstr["value"]

        # pre-process edstr["var"]
        vars = edstr["var"]
        if isinstance(vars,list):
            vars = []
            for var in edstr["var"]:
                vars.append(resolve_var(var,value,variables,loc_variables))
            if add_english:
                if edstr["var"][0] in variables:
                    vars.append(f'"{variables[edstr["var"][0]]}"')  # append English string
        elif add_english:
            var = vars
            vars = []
            vars.append(resolve_var(var,value,variables,loc_variables))
            if var in variables:
                vars.append(f'"{variables[var]}"')
        else:
            vars = resolve_var(vars,value,variables,loc_variables)

        if isinstance(vars,list):  # multiple translations
            # ( @title = "${var[0]}" or $title = "${var[1]} ... ")
            # contains(@title,"${var[0]}" or )
            condline = "("
            orstr = ""
            #edit(f"Debug: vars={vars}")
            for var in vars:
                ref = openstr + edstr["g1"] + edstr["g2"] + var + closestr
                condline += orstr + ref
                orstr = " or "
            condline += ")"
            ref = outer_op + condline + outer_cl
            # print (f"ref={ref}")
        else:
            ref = outer_op + openstr + edstr["g1"] + edstr["g2"] + vars + closestr + outer_cl # @title = "${var}"
        newline = newline[:edstr["begin"]] + ref + newline[edstr["end"]:]

    # print(f"edit_line:outer_op={outer_op} openstr={openstr} closestr={closestr} outer_cl={outer_cl}")
    # sys.stdout.write('"%s"\n"%s"\n' % (line.strip('\n'),newline.strip('\n')))

    return newline

def is_placeholder(value):
    n = placeholder_pat.match(value)
    if n: # placeholder only
        #print(f"placeholder={value}")
        return True
    if value[0:2] == '${' or value == '(_____placeholder_____)' or value == 'placeholdervar' : # var reference
        return True
    return False

# exracor for XPATH file
def extract_xpath(path,variables=None,verbose=False,all_variables=None,playwright=False,fuzzy_match=False):
    DIAG = False
    propfile = ""
    syspropfile = ""
    sysprop = []

    if not os.path.exists(path):
        print (f"{path} does not exist.")
        return None, None

    with codecs.open(path,'r',encoding='utf-8') as fp:
        lines = fp.readlines()

    keys = {}  # store new keys
    variable_section = False
    nxpath = 0
    for line in lines:
        line = line.strip('\n')
        # check whether a xpath contains localizalbe string

        m = text_pat.search(line)
        tx_sw = bool(m)
        if DIAG:
            print (f"{tx_sw}: {line}")
        if not tx_sw:
            continue
        found, line2, props , vars = extract_selector_xpath(line,variables,all_variables,verbose=verbose,fuzzy_match=fuzzy_match)
        if not found:
            print (f"!{line2}")
        nxpath += 1
        # if nxpath == 24:
        #     print (f"{found} line2={line2}\n\tprops={props} vars={vars}")
        if found:
            #syspropfile += update_props_vars(line2,nxpath,props,vars)
            syspropfile += f"xpath{nxpath} = {line}\n"
            for var in vars:
                if var["key"] not in keys:
                    keys[var["key"]] = 0
                    propfile += f'{var["key"]} = {var["value"]}\n'
                keys[var["key"]] += 1
        else:
            print (f"No translatable string: {line2}")

    return syspropfile, propfile

namevalue = re.compile(r'(?P<N>xpath\d+) = (?P<V>.*)')
def localize_xpath(lines0, all_variables, locale=None, add_english=False,fuzzy_match=False):
    propfile = ""
    variables = all_variables["variables"]["en"]
    lines = lines0.splitlines()
    for line in lines:
        m = namevalue.match(line)
        if not m:
            propfile += f"{line}\n"
        else:
            name = m.group('N')
            value = m.group('V')
            found, translated, props , vars = extract_selector_xpath(value,variables,all_variables,
                verbose=False,locale=locale,add_english=add_english,fuzzy_match=fuzzy_match)
            #print(f"{found} props={props} vars={vars}\n translated={translated}")
            propfile += f"{name} = {translated}\n"
    return propfile

def var_fuzzy_match(label,variables=None,verbose=False):
    #
    # neee to handle multiple matches
    #
    value = label
    nhit = 0
    tokens = label.split(' ')
    if len(tokens)<2:  # only one token
        return value, 0
    var = ' '.join(tokens[0:-1])
    print (f"tokens={tokens} token={var}")
    value0 , nhit = var_reference(var,variables,hint="prefix",verbose=True)
    #print (f"\tvalue0={value0} value={value} nhit={nhit}")
    if nhit>0:
        return value0, nhit
    return value, nhit

def resolve_fuzzy_variable(key,value,variables,loc_variables):

    tokens = value.split(' ')
    if key.endswith("*"):
        key = key[0:-1]  # strip trailing '*'
    if key.endswith(".prefix"):
        key = key[0:-(len(".prerix"))]  # need to resolve placeholder
        value = loc_variables[key]
    else:
        value = loc_variables[key] + ' {0}'

    #tokens = variables[key].split(' ')
    print(f"resolve_fuzzy_variable: key={key} value={value} tokens={tokens}")
    value = re.sub(r'{\d}',tokens[-1],value)

    return value

if __name__ == "__main__":

    text ='''${Obj_DE_ZeroState_Svg}    xpath://*[text()= "No data is selected."] '''
    m = text_pat.search(text)
    if m:
        print (f'{m.group("T")}')
    else:
        print ("not found.")
