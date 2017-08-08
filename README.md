# Petrel
<img src = "logo.png" height = 300px>
<br>
<br>
The primary objective of MarkerSub is to develop an automated data extraction pipeline from published scientific publications (via PubMed) and subsequently populate Markerville, a web-based biomarker database constructed by Mallick Lab. Using the natural language processing (NLP) and machine learning elements of Stanford-based Snorkel and DeepDive, this software pipeline programmatically reads through biomedical literature, aggregates the data, and uploads it to Markerville. Through this tool's efficient (and hopefully accurate) identification of biomarkers from thousands of works, the hope is to render the process of manually gathering biomarker and patient data unnecessary.

The initial version of the software will extract biomarkers along with a few other data points such as associated conditions, detection medium, detection methodologies, associated drugs and therapies, and macromolecular type — all from abstracts. As further development occurs however, the software will also be able to analyze full-text documents, thereby opening up the scope to gather data about disease stagining and clinical trials (number of trials, number of patients sampled, levels of the biomarkers in the patients, and other generalized patient background information). By repeatedly training the software using Snorkel’s machine learning features, the accuracy of the software will be maximized and bias minimized.

Maintained by Gautam Machiraju and Mallick Lab summer interns. A joint project between Mallick Lab, Stanford School of Medicine and Stanford's Info Lab, Department of Computer Science.
