import pandas as pd
from snorkel.models import StableLabel
from snorkel.db_helpers import reload_annotator_labels
from snorkel.models import GoldLabel


def load_external_labels(session, candidate_class, column1_title, column2_title, filepath, candidates, annotator_name='gold'):
    gold_labels = pd.read_csv(filepath, sep="\t")
    for index, row in gold_labels.iterrows():    

        # We check if the label already exists, in case this cell was already executed
        context_stable_ids = "~~".join([row[column1_title], row[column2_title]])
        query = session.query(StableLabel).filter(StableLabel.context_stable_ids == context_stable_ids)
        query = query.filter(StableLabel.annotator_name == annotator_name)
        # print context_stable_ids
        if query.count() == 0:
                session.add(StableLabel(
                    context_stable_ids=context_stable_ids,
                    annotator_name=annotator_name,
                    value=row['label']))

	
        # Because it's a symmetric relation, load both directions...
        context_stable_ids = "~~".join([row[column1_title], row[column2_title]])
        query = session.query(StableLabel).filter(StableLabel.context_stable_ids == context_stable_ids)
        query = query.filter(StableLabel.annotator_name == annotator_name)
        if query.count() == 0:
                session.add(StableLabel(
                    context_stable_ids=context_stable_ids,
                    annotator_name=annotator_name,
                    value=row['label']))
    for c in candidates:
        print c.biomarker.get_stable_id()
        print c
        candidate_label = c[0].get_stable_id() + "~~" + c[1].get_stable_id()
        query = session.query(StableLabel).filter(StableLabel.context_stable_ids == candidate_label)
        query = query.filter(StableLabel.annotator_name == annotator_name)
        if query.count() == 0:
            session.add(StableLabel(
                context_stable_ids=candidate_label,
                annotator_name=annotator_name,
                value=-1))


    # Commit session
    session.commit()
	
    # Reload annotator labels
    reload_annotator_labels(session, candidate_class, annotator_name, split=1, filter_label_split=False)
    reload_annotator_labels(session, candidate_class, annotator_name, split=2, filter_label_split=False)
