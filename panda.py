from numpy import sort_complex
import pandas as pd
import sqlite3, re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

import joblib

def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""
    
    #use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []
    
    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        
        #keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    #create a tuples of feature,score
    #results = zip(feature_vals,score_vals)
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    
    return results

def pre_process(text):
    text = text.lower()
    #re.sub("(\\d|\\W)+"," ",text)
    return text

def get_stop_words(stop_file_path):
    """load stop words """
    
    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return frozenset(stop_set)

stopwords=get_stop_words("stopwords.txt")

#sqlite
con = sqlite3.connect('linkedin.db')

df = pd.read_sql_query("SELECT * from vacancies_e", con)

docs = df.description[df.language == "en"].tolist()

docs = [pre_process(x) for x in docs]

vect = CountVectorizer(max_df=0.70,stop_words=stopwords,max_features=1000)
word_count_vect = vect.fit_transform(docs)

print(list(vect.vocabulary_.keys())[:10])

tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
tfidf_transformer.fit(word_count_vect)


description = ["""We are looking for an organized,  analytical and skilled individual to join our team as a Back-end developer for our PIM & WEB projects (back-end) implementations & integrations.

    you translate the needs and questions of the customer into practical applications
    you build software solutions that provide significant added value
    you are responsible for end-to-end development of applications
    you think along to deliver optimal system archtectural solutions 

    you have experience in building and/or integrating API’s
    you have in-depth knowledge about at least Java, JavaScript, MS SQL, jQuery, HTML, CSS""","""We zijn op zoek naar freelance Java consultants om in te schakelen op projecten en opdrachten bij onze klanten. We ontvangen dagelijks opdrachten, waarvoor we vaak een beroep doen op ons netwerk. Solliciteer nu en sluit je aan bij ons netwerk van freelancers!

Als Java developer ben je verantwoordelijk voor het ontwikkelen van high-quality softwareapplicaties. Je werkt samen met architecten en businessanalisten, en je houdt rekening met de user requirements, zodat de software voldoet aan het gevraagde ontwerp. Je maakt gebruik van innovatieve technologieën en werkt volgens de agile-methodiek.

Wie we zoeken


    Je bent gepassioneerd door Java-technologie
    Je hebt ervaring met Spring stack, Spring Boot, Spring MVC, Spring Data en eventueel Spring Cloud
    Ervaring met Netflix OSS is een pluspunt
    Je hebt ervaring met geautomatiseerd testen: unit testing, integratie testen en acceptatie testen
    Je kan werken met applicatieservers en -containers en weet hoe je tools als Git, Jenkins, Sonar en Maven kan gebruiken
    Je kent cloud-platforms zoals Amazon Web Services, Google Compute Engine of Azure, kennis van Kubernetes, OpenShift of Cloud Foundry is een pluspunt
    Je bent vertrouwd met cloud native architectures, zoals microservices
    Je bent vertrouwd met methodieken zoals DevOps, Scrum en Kanban
    Je kan communiceren in het Nederlands en Engels



Wat we bieden


    Je draagt bij tot uitdagende projecten bij top internationale en Belgische bedrijven uit diverse sectoren
    Je werkt in een hightech omgeving met focus op kennis en innovatie, een open no-nonsense bedrijfscultuur met ruimte voor eigen initiatief
    Binnen Ordina beschikken we over een groot portfolio aan klanten met elk hun specifieke aspecten. Samen kijken we naar het project dat het beste bij jou past
    We vinden het belangrijk dat onze freelancers een eerlijk, marktconform tarief krijgen, we willen een lange termijn relatie opbouwen, waardoor niet enkel de klant maar ook jij er beter van wordt
    We streven ernaar om onze freelancers correct te betalen, zo kan je zeker zijn van een stipte uitbetaling van je factuur en dat elke maand opnieuw
    Als freelancer word je behandeld als een interne consultant, door onze krachten te bundelen helpen we iedere dag mee aan een beter IT-landschap""", """Function


Sopra Banking Software is looking for an Android developer to reinforce our Developers team on a project based in the center of Brussels.

The assignments of the Developer include (but are not limited to):

    Design and build advanced applications for the Android platform.
    Collaborate with cross-functional teams to define, design, and ship new features.
    Unit-test code for robustness, including edge cases, usability, and general reliability.
    Work on bug fixing and improving application performance.
    Continuously discover, evaluate, and implement new technologies to maximize development efficiency.


Profile


    Education: Bachelor’s in computer sciences.
    0 – 2 years of software development experience.
    Android development skills with experience in Kotlin.
    Team player and good autonomy.
    Good organization.
    Strong analytical and problem solving skills.


Language


    Fluent in English and French is mandatory.


Offer


    A young and dynamic environment;
    A fun team;
    Clearly defined growth possibilities on multiple national and international projects;
    Sopra Banking University foresees trainings available throughout the entire career;
    Attractive financial package including interesting compensation & benefits such as an extended insurance package, a competitive salary and a range of employee benefits (company car, fuel card…).""", """
    As a Deloitte Digital Application Developer you will help our clients identify and solve their challenges through technology. You will join a team of experienced consultants to perform exciting projects in the area of customer technologies. You will be able to work with some of the best architects, developers and functional experts.

You will be involved in designing and developing innovative CRM applications for our clients, turning challenging business requirements into actionable technical solutions that fit in the client's IT landscape. You will be involved in designing and developing complex application components. Within our Deloitte Digital team, developers are not people who are locked in a room to churn out code to match a large paper based specification. They need to work alongside our clients across the entire project life-cycle.

Your future

As you become more senior, you will:

    acquire deeper knowledge on CRM business processes, CRM technologies and Deloitte methodologies;
    learn everything about “agile” approaches;
    have the opportunity to take on roles with more responsibilities, such as a Technical Lead, Integration/Migration Lead or Technical Architect;
    guide new joiners on projects and help them further develop their competencies.

Your Profile

    You have a strong interest in technology and understand how it can be used to enable business processes;
    You have knowledge of at least one of the following programming languages: java, C++, .net or C#;
    Knowledge of one of the following web application development technologies: HTML, CSS or Ajax is a an added value;
    You are a flexible, eager to learn and have a strong team spirit;
    You feel comfortable in new environments and are not afraid to speak up;
    You are open-minded and willing to learn (e.g. about Salesforce.com, Deloitte Tools and Methodologies);
    You are fluent in Dutch and/or French and have a good working knowledge in English."""]
joblib.dump(tfidf_transformer, 'tfidf.pkl')
joblib.dump(vect, 'vect.pkl')
# you only needs to do this once, this is a mapping of index to 
feature_names = vect.get_feature_names()

#generate tf-idf for the given document
tf_idf_vector = tfidf_transformer.transform(vect.transform([pre_process(description[1])]))
joblib.dump(tfidf_transformer, 'model.pkl')
#sort the tf-idf vectors by descending order of scores
sorted_items=sort_coo(tf_idf_vector.tocoo())

#extract only the top n; n here is 10
keywords=extract_topn_from_vector(feature_names,sorted_items,10)

# now print the results
print("\n=====Doc=====")
print(description[1])
print("\n===Keywords===")
for k in keywords:
    print(k,keywords[k])