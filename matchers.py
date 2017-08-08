from snorkel import *
from snorkel.matchers import *
import pickle
import sys
import os
import cPickle

# These matchers are either based on Regex scans or DB matches via Snorkel
prefixes = [['Y', 'yotta'], ['Z', 'zetta'], ['E', 'exa'], ['P', 'peta'], ['T', 'tera'], ['G', 'giga'], ['M', 'mega'], ['k', 'kilo'], ['h', 'hecto'], ['da', 'deka'], ['d', 'deci'], ['c', 'centi'], ['\u03bc', 'micro'], ['n', 'nano'], ['p', 'pico'], ['f', 'femto'], ['a', 'atto'], ['z', 'zepto'], ['y', 'yocto']]
length_unit = ['m', 'meter']
area_unit = ['m2', 'square ', 'meter']
volume_unit = ['m3', 'cubic ', 'meter']
liquid_volume_unit = ['L', 'liter']
mass_unit = ['g', 'gram']
conc_unit = ['mol', 'moles']

all_prefixes_units = [['Ym', 'yottameter'], ['Zm', 'zettameter'], ['Em', 'exameter'], ['Pm', 'petameter'], ['Tm', 'terameter'], ['Gm', 'gigameter'], ['Mm', 'megameter'], ['km', 'kilometer'], ['hm', 'hectometer'], ['dam', 'dekameter'], ['dm', 'decimeter'], ['cm', 'centimeter'], ['\\u03bcm', 'micrometer'], ['nm', 'nanometer'], ['pm', 'picometer'], ['fm', 'femtometer'], ['am', 'attometer'], ['zm', 'zeptometer'], ['ym', 'yoctometer'], ['Ym2', 'square yottameter'], ['Zm2', 'square zettameter'], ['Em2', 'square exameter'], ['Pm2', 'square petameter'], ['Tm2', 'square terameter'], ['Gm2', 'square gigameter'], ['Mm2', 'square megameter'], ['km2', 'square kilometer'], ['hm2', 'square hectometer'], ['dam2', 'square dekameter'], ['dm2', 'square decimeter'], ['cm2', 'square centimeter'], ['\\u03bcm2', 'square micrometer'], ['nm2', 'square nanometer'], ['pm2', 'square picometer'], ['fm2', 'square femtometer'], ['am2', 'square attometer'], ['zm2', 'square zeptometer'], ['ym2', 'square yoctometer'], ['Ym2', 'cubic yottameter'], ['Zm2', 'cubic zettameter'], ['Em2', 'cubic exameter'], ['Pm2', 'cubic petameter'], ['Tm2', 'cubic terameter'], ['Gm2', 'cubic gigameter'], ['Mm2', 'cubic megameter'], ['km2', 'cubic kilometer'], ['hm2', 'cubic hectometer'], ['dam2', 'cubic dekameter'], ['dm2', 'cubic decimeter'], ['cm2', 'cubic centimeter'], ['\\u03bcm2', 'cubic micrometer'], ['nm2', 'cubic nanometer'], ['pm2', 'cubic picometer'], ['fm2', 'cubic femtometer'], ['am2', 'cubic attometer'], ['zm2', 'cubic zeptometer'], ['ym2', 'cubic yoctometer'], ['YL', 'yottaliter'], ['ZL', 'zettaliter'], ['EL', 'exaliter'], ['PL', 'petaliter'], ['TL', 'teraliter'], ['GL', 'gigaliter'], ['ML', 'megaliter'], ['kL', 'kiloliter'], ['hL', 'hectoliter'], ['daL', 'dekaliter'], ['dL', 'deciliter'], ['cL', 'centiliter'], ['\\u03bcL', 'microliter'], ['nL', 'nanoliter'], ['pL', 'picoliter'], ['fL', 'femtoliter'], ['aL', 'attoliter'], ['zL', 'zeptoliter'], ['yL', 'yoctoliter'], ['Yg', 'yottagram'], ['Zg', 'zettagram'], ['Eg', 'exagram'], ['Pg', 'petagram'], ['Tg', 'teragram'], ['Gg', 'gigagram'], ['Mg', 'megagram'], ['kg', 'kilogram'], ['hg', 'hectogram'], ['dag', 'dekagram'], ['dg', 'decigram'], ['cg', 'centigram'], ['\\u03bcg', 'microgram'], ['ng', 'nanogram'], ['pg', 'picogram'], ['fg', 'femtogram'], ['ag', 'attogram'], ['zg', 'zeptogram'], ['yg', 'yoctogram']]
medium = ['blood', 'blood plasma', 'serum', 'urine', 'cell', 'saliva', 'amniotic fliud', 'tears', 'breast milk', 'vitreous humor', 'aqueous humor', 'cerebrospinal fluid', 'bile', 'cerumen', 'chyle', 'lymph', 'interstitial fluid', 'sera', 'ascites', 'CSF', 'sputum', 'bone marrow', 'synovial fluid', 'cerumen', 'broncheoalveolar lavage fluid', 'semen', 'postatic fluid', 'cowper\'s fluid',
          'pre-ejaculatory fluid', 'female ejaculate', 'sweat', 'feces', 'fecal matter', 'hair', 'cyst fluid', 'pleural fluid', 'peritoneal fluid', 'pericardinal fluid', 'chyme', 'menses', 'pus', 'sebum', 'vomit', 'vaginal secretion', 'stool water', 'pancreatic juice', 'pancreatic fluid', 'lavage fluids', 'bronchopulmonary aspirates', 'blastocyl cavity fluid', 'umbilical chord blood']

import itertools
all_lengths = []
all_areas = []
all_volumes = []
all_lvolumes = []
all_masses = []
all_concs = []

for prefix in prefixes:
    perms_lengths = map(''.join, itertools.product(prefix, length_unit))
    perms_areas = map(''.join, itertools.product(prefix, area_unit))
    perms_volumes = map(''.join, itertools.product(prefix, volume_unit))
    perms_lvolumes = map(''.join, itertools.product(
        prefix, liquid_volume_unit))
    perms_masses = map(''.join, itertools.product(prefix, mass_unit))
    perms_concs = map(''.join, itertools.product(prefix, conc_unit))

    all_lengths.extend(perms_lengths)
    all_areas.extend(perms_areas)
    all_volumes.extend(perms_volumes)
    all_lvolumes.extend(perms_lvolumes)
    all_masses.extend(perms_masses)
    all_concs.extend(perms_concs)

# clean up lengths
all_lengths3s = all_lengths[3::4]
all_lengths4s = all_lengths[4::4]
all_lengths = [all_lengths[0]] + all_lengths3s + all_lengths4s

# clean up areas
all_areas = all_areas[0::2]
for prefix in prefixes:
    all_areas.append('square ' + prefix[1] + 'meter')

# clean up volumes
all_volumes = all_volumes[0::2]
for prefix in prefixes:
    all_volumes.append('cubic ' + prefix[1] + 'meter')

# clean up liquid volumes
all_lvolumes3s = all_lvolumes[3::4]
all_lvolumes4s = all_lvolumes[4::4]
all_lvolumes = [all_lvolumes[0]] + all_lvolumes3s + all_lvolumes4s

# clean up masses
all_masses3s = all_masses[3::4]
all_masses4s = all_masses[4::4]
all_masses = [all_masses[0]] + all_masses3s + all_masses4s


# make concentrations: masses/volumes
all_concs3s = all_concs[3::4]
all_concs4s = all_concs[4::4]
all_concs = [all_concs[0]] + all_concs3s + all_concs4s

for item in all_masses:
    all_concs.append(item + '/mol')
    all_concs.append(item + ' per mol')
    all_concs.append(item + '/L')
    all_concs.append(item + ' per liter')
    
unitsList = all_lengths + all_areas + all_volumes + all_lvolumes + all_masses + all_concs   

def getBiomarkerMatcher():
    with open('databases/markerData.pickle', 'rb') as f:
        markerDatabase = pickle.load(f)
    marker_dm = DictionaryMatch(d=markerDatabase, ignore_case=False)
    marker_regex = RegexMatchEach(
        rgx=r'(^|(?<=\s))[A-Za-z][A-Z1-9-]{2,}', ignore_case=False, attrib='words')
    matcher = Union(marker_regex, marker_dm)
    return matcher

def getUnitsMatcher():
    with open('databases/unitsDatabase.pickle', 'rb') as f:
            unitsDatabase = pickle.load(f)
    #units_regex = RegexMatchEach(rgx=r'(?<=\s)[a-zA-Z]{1,2}[1-9]?(?=[\s\,\.])|(?<=\s)[a-zA-Z]{1,2}[1-9]?[\/]{1}[a-zA-Z]{1,2}[1-9]?(?=[\s\.\,])', ignore_case=False, attrib='words')
    #matcher = Union(units_regex, units_dm)
    units_dm = DictionaryMatch(d=unitsDatabase, ignore_case=True)
    return units_dm #matcher  # unit_regex


def getLevelsMatcher():
    #normal_syntax_regex = RegexMatchEach(rgx=r'(?<=[^a-zA-Z:;])[0-9]+[-,\.]?[0-9]+', ignore_case=False, attrib='lemmas')
   # range_syntax_regex = RegexMatchSpan(normal_syntax_regex, rgx=r'[0-9]+[\W^;]?[0-9]+\s[()][^\sa-zA-Z()]+[()]', ignore_case=False, attrib='text')
    #(\d+(?:\.\d*)?|\.\d+)
    levels_regex = RegexMatchEach(rgx=r'((\d+(?:\.\d*)?|\.\d+)+-(\d+(?:\.\d*)?|\.\d+))|(\d+(?:\.\d*)?|\.\d+)', ignore_case=False, attrib='words')
    return levels_regex  


def getMeasurementTypeMatcher():
    noun_regex = RegexMatchEach(
        rgx=r'[A-Z]?NN[A-Z]?', ignore_case=True, attrib='poses')
    complete_obj_regex = RegexMatchSpan(
        noun_regex, rgx=r'[J]{2,}\sNN[A-Z]?', ignore_case=True, attrib='poses')
    # CE = Union(noun_regex, complete_obj_regex)
    return complete_obj_regex

def getTestSetMatcher():
    noun_regex = RegexMatchEach(
        rgx=r'[A-Z]?NN[A-Z]?', ignore_case=True, attrib='poses')
    complete_obj_regex = RegexMatchSpan(
        noun_regex, rgx=r'[J]{2,}\sNN[A-Z]?', ignore_case=True, attrib='poses')
    return complete_obj_regex


def getDiseaseMatcher():
    with open('databases/diseaseAbbreviationsDatabase.pickle', 'rb') as f:
        diseaseAbb = pickle.load(f)

    with open('databases/diseaseDatabase.pickle', 'rb') as f:
        diseaseDictionary = pickle.load(f)
    
    with open('databases/expandedDiseaseDatabase.pkl', 'rb') as f:
        expDisease = pickle.load(f)
    
    with open('databases/wikiData.pkl', 'rb') as f:
        wikiDiseases = pickle.load(f)
    if('latex' in wikiDiseases):
        print "ASDF"
    else:
        print "ASDFASDF"
    
    DiseaseMatch = DictionaryMatch(d=diseaseDictionary, ignore_case=True)
    AbbMatch = DictionaryMatch(d=diseaseAbb, ignore_case=False)
    ExpMatch = DictionaryMatch(d=expDisease, ignore_case = True)
    OwlMatch = DictionaryMatch(d=wikiDiseases, ignore_case = True)
    temp = Union(DiseaseMatch, AbbMatch)
    temp2 = Union(ExpMatch, OwlMatch)
    #return Union(temp, temp2)
    return OwlMatch


def getDrugMatcher():
    with open('databases/drugDatabase.pickle', 'rb') as f:
        drugDictionary = pickle.load(f)
    drug_regex = RegexMatchEach(
        rgx=r'[\w\-]+(afil|asone|bicin|bital|caine|cillin|cycline|dazole|dipine|dronate|eprazole|fenac|floxacin|gliptin|glitazone|iramine|lamide|mab|mustine|mycin|nacin|nazole|olol|olone|olone|onide|oprazole|parin|phylline|pramine|pril|profen|ridone|sartan|semide|setron|setron|statin|tadine|tadine|terol|thiazide|tinib|trel|tretin|triptan|tyline|vir|vudine|zepam|zodone|zolam|zosin)', ignore_case=True, attrib='words')
    DrugMatch = DictionaryMatch( d=drugDictionary, ignore_case=False)
    matcher = Union(drug_regex, DrugMatch)
    return matcher


def getMediumMatcher():
    with open('databases/mediumDatabase.pickle', 'rb') as f:
        mediumDatabase = pickle.load(f)

    mediumMatcher = DictionaryMatch(d=mediumDatabase, ignore_case=True)
    return mediumMatcher


def getTypeMatcher():
    with open('databases/typesDatabase.pickle', 'rb') as f:
        typeDatabase = pickle.load(f)

    typeMatcher = DictionaryMatch(d=typeDatabase, ignore_case=True)
    return typeMatcher


# Utility Functions:
#--------------------

def addDiseaseBases(EE, diseaseDictionary, final_article_str):
    counter = 0
    listCounter = 0
    wordIndex = 0
    currentPos = ''
    disease_candidates_edits = []

    for entity in EE:
        disease_index = entity.idxs[0]

        if disease_index is not 0:
            sentenceWords = entity.pre_window(
                attribute='words', n=disease_index)
            diseaseName = unicodedata.normalize('NFKD', ' '.join(
                entity.mention(attribute='words'))).encode('ascii', 'ignore')
            sentencePos = entity.pre_window(attribute='poses', n=disease_index)
            normalized_Pos = unicodedata.normalize(
                'NFKD', sentencePos[0]).encode('ascii', 'ignore')

            if normalized_Pos == 'CC':
                # get base of disease(tumor,cancer)
                disease_base = ' ' + \
                    entity.mention(attribute='words')[
                        len(entity.idxs) - 1] + ' '
                normalized_disease_base = unicodedata.normalize(
                    'NFKD', disease_base).encode('ascii', 'ignore')
                sentenceWords.reverse()
                joined_sentenceWords = ' '.join(sentenceWords)
                normalized_sentenceWords = unicodedata.normalize(
                    'NFKD', joined_sentenceWords).encode('ascii', 'ignore')
                normalized_unjoined_sentenceWords = []

                for sentence in sentenceWords:
                    normalized_sentence = unicodedata.normalize(
                        'NFKD', sentence).encode('ascii', 'ignore')
                    normalized_unjoined_sentenceWords.append(
                        normalized_sentence)

                cutSentence = ' '.join(sentenceWords[0:len(sentenceWords) - 1])
                normalized_cutSentence = unicodedata.normalize(
                    'NFKD', cutSentence).encode('ascii', 'ignore')
                sentenceIdx = substringIndex(
                    final_article_str, normalized_unjoined_sentenceWords)
                indicesOfAnd = [(m.start(0)) for m in re.finditer(
                    'and', normalized_sentenceWords)]
                numberOfCommas = len([(m.start(0)) for m in re.finditer(
                    ',', normalized_sentenceWords)])  # commas add one extra whitespace

                # add sentence Index + Index of And - 1 - number of commas
                editIdx = sentenceIdx + \
                    indicesOfAnd[len(indicesOfAnd) - 1] - numberOfCommas

                for disease_candidate in diseaseDictionary:
                    normalized_disease_candidate_name = unicodedata.normalize(
                        'NFKD', disease_candidate).encode('ascii', 'ignore')
                    if normalized_disease_candidate_name.lower() in (normalized_cutSentence + normalized_disease_base).lower():
                        disease_candidates_edits.append(
                            [editIdx, normalized_cutSentence, normalized_disease_base])  # EDITED
                        listCounter = listCounter + 1

        counter = counter + 1

    disease_candidates_edits = removeRepeats(disease_candidates_edits)
    disease_candidates_edits.sort()
    # reverse so that we edit the article back-front to avoid index errors
    disease_candidates_edits.reverse()
    counter = 0

    for edit in disease_candidates_edits:
        edit_str_addition = edit[2]
        edit_index = edit[0]
        final_article_str = final_article_str[
            0:edit_index] + edit_str_addition + final_article_str[edit_index:len(final_article_str)]
        counter = counter + 1

    return final_article_str


def substringIndex(text, listWords):
    end = -3
    candidate_index = -2
    word = listWords[0]
    allIndices = [m.start() for m in re.finditer(word, text)]

    for index in allIndices:
        end = substringIndex_help(text, listWords, index)

        if (end is not -1 and end is not None):
            candidate_index = index
            return candidate_index

    return candidate_index


def substringIndex_help(text, listWords, index):
    if len(listWords) is 0:
        return 0
    elif len(listWords) is 1:
        withinRange = text[index:index + 15 + len(listWords[0])]
        if listWords[0] in withinRange:
            index = withinRange.index(listWords[0])
            return substringIndex_help(text, [], index)
        else:
            return -1
    else:
        parsedPaper = text[index:]
        withinRange = text[index:index +
                           len(listWords[0]) + 15 + len(listWords[1])]
        if listWords[1] in withinRange:
            index = withinRange.index(listWords[1])
            return substringIndex_help(parsedPaper, listWords[1:], index)
        else:
            return -1


def removeRepeats(list):
    counter = 1
    case = None
    for edit in list:
        for check in list[counter:]:
            if edit[0] is check[0]:  # If the two objects have the same edit index
                list.remove(check)
            counter = counter + 1
    return list
