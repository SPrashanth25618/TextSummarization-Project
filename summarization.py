import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

# Load SpaCy English model
nlp = spacy.load('en_core_web_sm')

def summarize_text(text, summary_percent=0.3):
    """
    Generate a summary of the input text using extractive summarization.
    
    Args:
        text (str): Input text to summarize
        summary_percent (float): Percentage of original sentences to include in summary
        
    Returns:
        str: Generated summary
    """
    # Process the text
    doc = nlp(text)

    # Calculate word frequencies
    word_frequencies = {}
    stopwords = list(STOP_WORDS)
    punctuation_set = set(punctuation) | {'\n'}
    
    for word in doc:
        word_text = word.text.lower()
        if word_text not in stopwords and word_text not in punctuation_set:
            word_frequencies[word_text] = word_frequencies.get(word_text, 0) + 1

    # Normalize frequencies
    if not word_frequencies:
        return ""
        
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] /= max_frequency

    # Score sentences
    sentence_scores = {}
    for sent in doc.sents:
        for word in sent:
            word_text = word.text.lower()
            if word_text in word_frequencies:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word_text]

    # Select top sentences
    select_length = max(1, int(len(list(doc.sents)) * summary_percent))
    summary_sentences = nlargest(select_length, sentence_scores, key=sentence_scores.get)

    return ' '.join([sent.text for sent in summary_sentences])