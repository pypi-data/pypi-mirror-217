from haystack_entailment_checker import EntailmentChecker
from haystack import Document

ec = EntailmentChecker()

doc = Document("My cat is lazy.")

print(ec.run("My cat is very active.", [doc]))
