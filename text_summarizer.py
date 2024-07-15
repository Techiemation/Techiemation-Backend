import spacy
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config, AutoTokenizer
#from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest


rawtext1 = """
"""


def summarizer(rawtext):
    
    print(len(rawtext))
    if len(rawtext) < 2000:
        print("Text is analyzed by Transformer")
        
        model = T5ForConditionalGeneration.from_pretrained('t5-small')
        tokenizer = AutoTokenizer.from_pretrained('t5-small', legacy=False)
        device = torch.device('cpu')

        preprocessed_text = rawtext.strip().replace('\n','')
        #print(preprocessed_text)
        t5_input_text = "summarize: " + preprocessed_text
        
        #print(t5_input_text)

        tokenized_text = tokenizer.encode(t5_input_text, return_tensors='pt', max_length=512, truncation=True).to(device)
        #print(tokenized_text)
        # summary_ids = model.generate(tokenized_text, min_length=30, max_length=200)
        # print(summary_ids)
        # summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
        summary_ids = model.generate(tokenized_text,
                                    num_beams=4,
                                    no_repeat_ngram_size=2,
                                    min_length=30,
                                    max_length=200,
                                    early_stopping=True)

        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        
        
        return summary, rawtext, len(rawtext.split(' ')), len(summary.split(' '))
        
        
    else:
        print("Text is analyzed by Spacy")
        stopwords = list(STOP_WORDS)
    # print(stopwords)
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(rawtext)
    # print(doc)

        tokens = [token.text for token in doc]

        word_freq = {}

        for word in doc:
            if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
                if word.text not in word_freq.keys():
                  word_freq[word.text] = 1
                else:
                  word_freq[word.text] += 1

        max_freq = max(word_freq.values())

        for word in word_freq.keys():
            word_freq[word] = word_freq[word] / max_freq

        sent_tokens = [sent for sent in doc.sents]

        sent_score = {}

        for sent in sent_tokens:
            for word in sent:
                if word.text in word_freq.keys():
                   if sent not in sent_score.keys():
                     sent_score[sent] = word_freq[word.text]
                   else:
                     sent_score[sent] += word_freq[word.text]

        select_length = int(len(sent_tokens) * 0.3)
        summary = nlargest(select_length, sent_score, key=sent_score.get)

        final_summary = [word.text for word in summary]
        summary = ' '.join(final_summary[::-1])  # Reverse the order of the summary

        return summary, doc, len(rawtext.split(' ')), len(summary.split(' '))


if __name__ == "__main__":
    text = "Dynamic languages you’re more familiar with, such as Ruby, Python, or JavaScript, you might not be used to compiling and running a program as separate steps. Rust is an ahead-of-time compiled language, meaning you can compile a program and give the executable to someone else, and they can run it even without having Rust installed. If you give someone a .rb, .py, or .js file, they need to have a Ruby, Python, or JavaScript implementation installed (respectively). But in those languages, you only need one command to compile and run your program. Everything is a trade-off in language design."
    print(summarizer(text))
