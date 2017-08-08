from snorkel import *
from snorkel.matchers import *
from snorkel.candidates import *
from snorkel.parser import *
from snorkel.models import *
import matchers
import cPickle
import pickle
import unicodedata

Disease = candidate_subclass('Disease', ['disease'])

def getBiomarkerUnitsRelations(sentences, session):
    biomarker_ngrams = Ngrams(n_max=1)
    unit_ngrams = Ngrams(n_max=10)

    # Retrieve Matchers:
    BM = matchers.getBiomarkerMatcher()
    U = matchers.getUnitsMatcher()

    CandidateExtractor_BM = CandidateExtractor(Disease, biomarker_ngrams, BM)
    CandidateExtractor_U = CandidateExtractor(Disease, unit_ngrams, U)

    # Create Relations Object
    possiblePairs = Relation(
        sentences, CandidateExtractor_BM, CandidateExtractor_U)

    return possiblePairs


def getBiomarkerLevelsRelations(sentences, session):
    biomarker_ngrams = Ngrams(n_max=1)
    levels_ngrams = Ngrams(n_max=15)

    # Retrieve Matchers:
    BM = matchers.getBiomarkerMatcher()
    L = matchers.getLevelsMatcher()

    CandidateExtractor_BM = CandidateExtractor(Disease, biomarker_ngrams, BM)
    CandidateExtractor_L = CandidateExtractor(Disease, levels_ngrams, L)

    # Create Relations Object
    possiblePairs = Relations(
        sentences, CandidateExtractor_BM, CandidateExtractor_L)

    return possiblePairs


def getBiomarkerMeasurementRelations(sentences, session):
    biomarker_ngrams = Ngrams(n_max=1)
    measurement_type_ngrams = Ngrams(n_max=5)

    # Retrieve Matchers:
    BM = matchers.getBiomarkerMatcher()
    MT = matchers.getMeasurementTypeMatcher()

    CandidateExtractor_BM = CandidateExtractor(Disease, biomarker_ngrams, BM)
    CandidateExtractor_MT = CandidateExtractor(
        Disease, measurement_type_ngrams, MT)

    # Create Relations Object
    possiblePairs = Relations(
        sentences, CandidateExtractor_BM, CandidateExtractor_MT)

    return possiblePairs


def getBiomarkerTestsetRelations(sentences, session):
    biomarker_ngrams = Ngrams(n_max=1)
    test_set_ngrams = Ngrams(n_max=10)

    # Retrieve Matchers:
    BM = matchers.getBiomarkerMatcher()
    TS = matchers.getTestSetMatcher()

    CandidateExtractor_BM = CandidateExtractor(Disease, biomarker_ngrams, BM)
    CandidateExtractor_TS = CandidateExtractor(Disease, test_set_ngrams, TS)

    # Create Relations Object
    possiblePairs = Relations(
        sentences, CandidateExtractor_BM, CandidateExtractor_TS)

    return possiblePairs


def getBiomarkerDiseaseRelations(session):
    # Processing the input data and converting to sentences
    # sentences = doc_parser.parseDoc(filename, session)
    #session = doc_parser.useCDRdata(session)
    
    corpus = session.query(Corpus).filter(Corpus.name == 'Training').one()
    sentences = set()
    for document in corpus:
        for sentence in document.sentences:
            sentences.add(sentence)
                 
    biomarker_ngrams = Ngrams(n_max=1)
    disease_ngrams = Ngrams(n_max=5)

    # Create the two matchers who have been defined in separate classes
    BM = matchers.getBiomarkerMatcher()
    DM = matchers.getDiseaseMatcher()

    # Building the CandidateExtractor: 
    # Combine candidate class, child context spaces, and matchers into the extractor
    ce = CandidateExtractor(Disease, [biomarker_ngrams, disease_ngrams], [BM, DM])
    
    # Running the CandidateExtractor: Retrieve cadidate set / relations 
    c = ce.extract(sentences, 'BD Training Candidates', session)
    print "Number of candidates:", len(c)
    session.add(c)
    session.commit()
    
    #repeat for dev and test!
    #for corpus_name in ['BD Development', 'BD Test']:
    #    corpus = session.query(Corpus).filter(Corpus.name == corpus_name).one()
    #    sentences = set()
    #    for document in corpus:
    #        for sentence in document.sentences:
    #            sentences.add(sentence)
    #    c = ce.extract(sentences, corpus_name + ' Candidates', session)
    #    session.add(c)
    #session.commit()
    
    return c, sentences, Disease, session


def getBiomarkerDrugRelations(filename, session):
    # Processing the input data and converting to sentences
    sentences = doc_parser.parseDoc(filename, session)

    biomarker_ngrams = Ngrams(n_max=1)
    drug_association_ngrams = Ngrams(n_max=5)

    BM = matchers.getBiomarkerMatcher()
    DAM = matchers.getDrugAssociationMatcher()
    
    ce = CandidateExtractor(Disease, [biomarker_ngrams, drug_association_ngrams], [BM, DAM])

    # possible pairs/relations (candidates)
    c = ce.extract(sentences, 'BDA Development Candidates', session)
    print "Number of candidates:", len(c)

    return c, sentences, Disease


def getBiomarkerMediumRelations(filename, session):
    # Processing the input data and converting to sentences
    sentences = doc_parser.parseDoc(filename, session)

    biomarker_ngrams = Ngrams(n_max=1)
    medium_ngrams = Ngrams(n_max=3)

    # Create the two matchers who have been defined in separate classes
    BM = matchers.getBiomarkerMatcher()
    MM = matchers.getMediumMatcher()

    CandidateExtractor_BM = CandidateExtractor(Disease, biomarker_ngrams, BM)
    CandidateExtractor_MM = CandidateExtractor(Disease, medium_ngrams, MM)

    # Create the relations using the two matchers
    possiblePairs = Relations(
        sentences, CandidateExtractor_BM, CandidateExtractor_MM)
    return possiblePairs


def getBiomarkerTypeRelations(filename, session):
    """
    Processing the input data and converting to sentences
    """
    sentences = doc_parser.parseDoc(filename, session)

    biomarker_ngrams = Ngrams(n_max=1)
    biomarker_type_ngrams = Ngrams(n_max=2)

    BM = matchers.getBiomarkerMatcher()
    TM = matchers.getBiomarkerTypeMatcher()

    CandidateExtractor_BM = CandidateExtractor(Disease, biomarker_ngrams, BM)
    CandidateExtractor_TM = CandidateExtractor(
        Disease, biomarker_type_ngrams, TM)

    # Running the CandidateExtractor to get Relations
    possiblePairs = Relations(
        sentences, CandidateExtractor_BM, CandidateExtractor_TM)

    return possiblePairs


# Above baseline extraction:
#---------------------------
# Generate all possible Multi-Relational objects from top 4 relation extractors

def AllLevelsRelationTuples(filename, session):
    sentences = doc_parser.parseDoc(filename, session)
    possiblePairs_BM_U = biomarkerUnitsRelations(sentences)
    possiblePairs_BM_L = biomarkerLevelsRelations(sentences)
    possiblePairs_BM_MT = biomarkerMeasurementRelations(sentences)
    possiblePairs_BM_TS = biomarkerTestsetRelations(sentences)

    # highly innefficient...fix!
    all = []
    for pair_BM_L in possiblePairs_BM_L:
        for pair_BM_TS in possiblePairs_BM_TS:
            if pair_BM_L.mention1(attribute='sent_id') == pair_BM_TS.mention1(
                    attribute='sent_id') and pair_BM_L.mention1(attribute='char_offsets') == pair_BM_TS.mention1(
                    attribute='char_offsets'):
                for pair_BM_MT in possiblePairs_BM_MT:
                    if pair_BM_L.mention1(attribute='sent_id') == pair_BM_MT.mention1(
                            attribute='sent_id') and pair_BM_L.mention1(attribute='char_offsets') == pair_BM_MT.mention1(
                            attribute='char_offsets'):
                        for pair_BM_U in possiblePairs_BM_U:
                            if pair_BM_L.mention1(attribute='sent_id') == pair_BM_U.mention1(
                                    attribute='sent_id') and pair_BM_L.mention1(
                                    attribute='char_offsets') == pair_BM_U.mention1(attribute='char_offsets'):
                                multiRelation = [
                                    pair_BM_L, pair_BM_TS, pair_BM_MT, pair_BM_U]
                                all.append(multiRelation)

    return all
