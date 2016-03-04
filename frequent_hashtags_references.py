#VBoga Authored on : 2/19/2016
#for Project IR.

import copy
import json
import pprint
import re   

#file = open("GOPDebate_tweets_file1.json", 'r')
#file = open("GOPDebate_tweets_file2.json", 'r')
file = open("election_tweets.json",'r')
file_objects = file.readlines()

loop_count = 0
json_objects = []
for file_object in file_objects:
    if file_object.isspace():
        pass
        #print("An empty line in the file, objects read: " + str(loop_count))
    else:
        file_object = file_object.strip('\n')
        json_objects.append(file_object)
    loop_count += 1

print("Total tweet count in the file:" + str(loop_count/2))

#formatted_tweets = open("formatted tweets.txt",'a')

count = 0
write_errors = 0

hashtable_for= {}
my_default = "HASH TABLE ERROR"
text_retweet_tries = 0
doc_count = 1
word_dictionary = {}

for json_object in json_objects:
    json_formatted = json.loads(json_object)
    tweet_keys = json_formatted.keys()
    for key in tweet_keys:
        #formatted_tweets.write("Text                   :"+json_formatted['text'] + "\n")
        key_string = str(key)
        my_value = json_formatted.get(key,"THIS_KEY_IS_ABSENT")
        if my_value == '0' or my_value == 'false' or my_value == "THIS_KEY_IS_ABSENT":
            pass
        else:
            if key_string == 'text' or key_string == 'retweeted_status':
                my_value = str(my_value)
                my_value = my_value.replace("'","")
                my_value = my_value.replace(","," ")
                my_value = my_value.replace(":"," ")
                my_value = re.sub('[:."!?;|]+', '', my_value)
                #my_value = my_value.lower() => Can't do this as we would miss some important hashtags
                words = my_value.split()
                unique_words = set(words)
                for word in unique_words:
                    if word[:1] == '#' or word[:1] == '@':
                        if word in word_dictionary.keys():
                            word_dictionary[word] +=  words.count(word)
                        else:
                            word_dictionary[word] = words.count(word)
                    else:
                        pass
                text_retweet_tries += 1
            else:
                pass
    count = count+1
    #if count == 100:
    #    break

#all_words = word_dictionary.keys()
#for word in all_words:
#    print("\n"+ word + " : "+ str(word_dictionary[word]))

top_most = 0
not_interested_words = []
#based on observation 
not_interested_words.append("RT")
not_interested_words.append("#GOPDebate")

#numbers and characters
not_interested_words.extend(['0','1','2','3','4','5','6','7','8','9'])
not_interested_words.extend(['-','X'])

not_interested_words.extend(['a', 'A'])
not_interested_words.extend(["an","An"])
not_interested_words.extend(["the","The"])

not_interested_words.extend(["to","To","from","From"])
not_interested_words.extend(["In","in"])
not_interested_words.extend(["on","of","for","by","from"])
not_interested_words.extend(["with","about","at","as","one","like","after"])
not_interested_words.extend(["we","We","you","You","I","our","am","Your","your"])
not_interested_words.extend(["I'm"])

not_interested_words.extend(["No", "no", "yes","Yes","only"])

#third person
not_interested_words.extend(["he","He","she","She"])
not_interested_words.extend(["they","They"])
not_interested_words.extend(["it","It","that","all"])
not_interested_words.extend(["His","his","her","Her","Him","him","my","My"])
not_interested_words.extend(["this","This"])
not_interested_words.extend(["has","had","have","hasn't","hadn't","haven't"])                  

#common_verbs
not_interested_words.extend(["is","Is","be","Be"])
not_interested_words.extend(["are","Are"])
not_interested_words.extend(["was","Was","Were","were"])

#conjuctives
not_interested_words.extend(["and","or","but","if","whether","so","So"])

#questions
not_interested_words.extend(["how","How","what","What","Who","who","whom","Whom"])
not_interested_words.extend(["Can","can","Could","could"])
not_interested_words.extend(["Can't","can't","Couldn't","couldn't"])                            
not_interested_words.extend(["Will","will","Would","would"])
not_interested_words.extend(["Should","should","shall","Shall"])
not_interested_words.extend(["Do","do","Don't","don't"])                             

#unwanted words
not_interested_words.extend(["just","now","know","after","After","hey","Hey","not"])
print(not_interested_words)

frequent_tags = open('frequent_tags.txt','a')

for w in sorted(word_dictionary, key = word_dictionary.get, reverse=True):
    if w in not_interested_words:
        continue
    else:
        #print(str(top_most+1) + ".  " + w + " : " + str(word_dictionary[w]))
        #print(w + " : " + str(word_dictionary[w]))
        try:
            frequent_tags.write(w + " " + str(word_dictionary[w]) + "\n")
        except:
            print("Couldn't write the tag:" + w)
            continue
        top_most += 1
        if top_most == 500:
            break
frequent_tags.close()

print(" Number of tweet texts and retweet texts parsed:" + str(text_retweet_tries)) 
print(" Number of tweets in json format parsed:" + str(count))
