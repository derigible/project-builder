'''
Created on Feb 11, 2015

@author: derigible
'''

from collections import OrderedDict as od
import templater.loader as disc

reserved_words = ("parent", "foot")
approved_block_types = ("inherit", "keepnested")

'''Tag type'''
TAG_TYPE = 0

'''Tag name'''
TAG_NAME = 1

'''Block reference'''
BLOCK_REF = 2

'''Block Length'''
BLOCK_LEN = 3

'''Extends Length'''
EXTENDS_LEN = 2

'''ENDBLOCK_LEN'''
ENDBLOCK_LEN = 2

def is_start_tag(c, i, item):
    '''
    Check if charcter is the beginning of a start tag. This will check if c = { and if c + item[i + 1] != %.
    
    This will raise a Syntax error under the following conditions:
    
    1) c = { and c + item[i + 1] != %
    
    @param c: the character to check
    @param i: the index of the character in the item
    @param item: the string to check
    '''
    if c == '{':
        if len(item) > i + 1 and item[i + 1] == '%':
            return True
        else:
            if len(item) > i + 1 and item[i + 1] == '{':
                return False
            tag = parse_tag(i, item)
            raise SyntaxError("Opening brace found at '{}' for tag '{}' without a modulo.".format(i, tag))
    return False 

def parse_tag(i, item):
    '''
    Parse the template tag. This will raise a Syntax error under the following conditions:
    
    1) A modulo is found and the next character is not a }
    2) An unexpected third word is used in the tag
    3) the word block is spelled wrong
    4) the reserved word parent is used as the tag
    5) more than three words are found in block
    6) if tag has inherits or keepnested and tag not found in parent or there is no parent
    7) another starting tag is found
    
    @param i: the position of the item to start in
    @param item: the string to parse
    @return (j, tag) where j is the end position of the tag in item, and tag is a dictionary 
    '''
    j = i
    tag = ""
    while j < len(item):
        if item[j] != '%' and item[j] != '}' and j < len(item):
            if not item[j] == ' ' or not item[j-1] == ' ':
                tag += item[j] #remove excess whitespace
            j += 1
            continue
        elif item[j] == '%' and item[j + 1] != '}':
            raise SyntaxError("Closing Modulo found in tag without closing brace char '{}' and line '{}'. Char '{}' precedes '{}'".format(j, item[i:j], item[j], item[j+1]))
        elif item[j] == '}':
            raise SyntaxError("Closing brace found in tag without closing modulo at char '{}' and line '{}'.".format(j, item[i:j]))   
        elif j == len(item):
            raise SyntaxError("Closing brace never found.") 
        elif item[j] == '{':
            raise SyntaxError("An opening tag or the { character was found inside an unclosed tag at '{}' for line '{}'.".format(j, item[i:j+1])) 
        j += 1 #increment to remove the }
        break #closing tag and such were found, break out of loop
    parts = list(filter(None, tag.split(' '))) #remove the empty strings from list
    if len(parts) > BLOCK_LEN:
        raise SyntaxError("Too many words were found in tag: '{}'".format(parts))
    if parts[TAG_NAME] in reserved_words:
        raise SyntaxError("Reserved word '{}' found as name of tag: '{}'".format(parts[TAG_NAME], parts))
    if parts[TAG_TYPE] == "extends":
        if len(parts) > EXTENDS_LEN:
            raise SyntaxError("Too many words in the extends tag (can only have 2, found '{}'): '{}'".format(len(parts), parts))
        #will raise error if not found
        parent = disc.load_template(parts[TAG_NAME])
        return j, {"type" : "extends", "parent" : parent, "tag" : parts[TAG_NAME]}
    if parts[TAG_TYPE] == "block":
        if len(parts) > BLOCK_LEN:
            if parts[BLOCK_REF] in approved_block_types:
                ref = parts[BLOCK_REF]
            else:
                raise SyntaxError("Unapproved block reference type. Found '{}' should be one of '{}'".format(parts[BLOCK_REF], approved_block_types))
        else:
            ref = None
        return j, {"type" : "block", "reference" : ref, "tag" : parts[TAG_NAME]}
    if parts[TAG_TYPE] == "endblock":
        if len(parts) > ENDBLOCK_LEN:
            raise SyntaxError("Too many words in endblock tag.")
        else:
            return j, {"type" : "endblock", "tag" : parts[TAG_NAME]}
    else:
        raise SyntaxError("Unknown value used to define block: '{}' in tag '{}'".format(parts[TAG_NAME], parts))
    
def add_tag(sections, tag_stack, tag, html):
    '''
    Takes the parts of the html parsing and adds them to the sections dictionary while performing all the necessary checks
    for consistency and correctness.
    
    @param sections: the sections of the template
    @param tag_stack: the stack that keeps track which parent tag is still open
    @param tag: the tag to add
    @param html: the html in the tag
    '''
    def add_tag(sections, stack, tag, html):
        tag["html"] = html
        sections[tag["tag"]] = tag
        stack.append(tag["tag"])
        return ""
    
    def end_tag(sections, stack, tag, html):
        if tag["tag"] in sections:
            top = tag_stack.pop()
            if tag["tag"] != top:
                raise KeyError("Missing endblock detected. Expected '{}' but found '{}'".format(tag["tag"], top))
            tag = sections[tag["tag"]]
            tag["html"] += html
            return ""
        else:
            raise KeyError("Endblock for tag '{}' has been found without a start block.".format(tag["tag"]))
        
    if tag["type"] == "extends":
        if "parent" in sections:
            raise SyntaxError("Cannot have more than one extends on a template.")
        sections["parent"] = tag["parent"]
        return html
    elif tag["tag"] in sections and tag["type"] == "block":
        raise KeyError("Block already created: '{}'".format(tag["tag"]))
    elif "parent" not in sections and tag["type"] == "block":
        sections["parent"] = {"type" : "head", html : html}
        return add_tag(sections, tag_stack, tag, html)
    elif tag["type"] == "block":
        return add_tag(sections, tag_stack, tag, html)
    elif tag["type"] == "endblock":
        return end_tag(sections, tag_stack, tag, html)
    else:
        raise RuntimeError("Something went wrong, tag type not recognized: '{}'".format(tag["type"]))
       
def parse_html_template(html):
    '''
    Returns the evaluated html as an ordered dictionary of sections. This dictionary follows this format:
    
    <block_name> - the key to the section defined as the block name
        - <type> - the type of tag it is
        - <html> - a string that preserves the order of the childblocks and the innerhtml defined there
        - <child_blocks> (optional)- an ordered dictionary of blocks with the key being the name of the block
        - <parent> (optional) - the parent block that this rests in, creating a two way link between block and childblock
        - <tag> - the same as the key
        
    @param html: the template as a string
    '''    
    sections = od()
    tag_stack = []
    out = ""
    in_html_tag = False
    i = 0
    while i < len(html): 
        c = html[i]
        if is_start_tag(c, i, html):
            i, tag = parse_tag(i + 2, html) #skip creation modulo
            out = add_tag(sections, tag_stack, tag, out)
        elif c == '%' and not in_html_tag:
            try:
                i, tag = parse_tag(i + 1, html)
            except SyntaxError:
                out += c #Modulo is allowed
                i += 1
            raise SyntaxError("Modulo found outside of html tag and without an opening brace at char '{}' for tag '{}'.".format(i, tag))
        elif c == '<':
            in_html_tag = True
            i += 1
            out += c
        elif c == '<' and in_html_tag:
            raise SyntaxError("Character < found inside of an html tag at char '{}'".format(i))
        elif c == '>':
            in_html_tag = False
            i += 1
            out += c
        else:
            out += c
            i += 1
        
    if tag_stack:
        raise KeyError("The following blocks did not have an end tag defined: '{}'".format(tag_stack))    
    if sections["parent"]["type"] == "head":
        sections["foot"] = {"type" : "foot", "html" : "out"}
    
    return sections        