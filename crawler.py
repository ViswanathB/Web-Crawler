#Author : Viswanath Boga
#Last Update : 2/22/2016
#Python twitter crawler using tweepy

import tweepy
import sys
import os
import json
import re
from tweepy import Stream
from tweepy.streaming import StreamListener

auth = tweepy.OAuthHandler("xyz") # add the keys here
auth.set_access_token("xxx")

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

key_indices_indendation = 40 # maximum key length is not more than this
entities_key_indices_indendation = 20

def for_user_inner_lists(my_value):
    formatted_tweets.write("\n *******************USER INFORMATION*******************\n")
    for key in my_value:
        formatted_tweets.write("\t\t"+str(key))
        key_string = str(key)
        key_string_length = len(key_string)
        spaces = key_indices_indendation - key_string_length
        while spaces > 0:
            formatted_tweets.write(" ")
            spaces -= 1
        my_value_string = my_value.get(key)
        if(key_string == 'description'):
            formatted_tweets.write("    :    **********" + str(my_value_string) + "**********\n")
        else:
            formatted_tweets.write("    :    " + str(my_value_string) + "\n")

def for_entities_inner_lists(my_value):
    for key in my_value:
        formatted_tweets.write("\t\t"+str(key))
        key_string = str(key)
        key_string_length = len(key_string)
        spaces = entities_key_indices_indendation - key_string_length
        while spaces > 0:
            formatted_tweets.write(" ")
            spaces -= 1
        formatted_tweets.write("    :    ")
        my_value_string = my_value.get(key)
        formatted_tweets.write(str(my_value_string) + "\n")
        
#api = tweepy.API(auth)

recursion_count = 0
word_dictionary = {}
text_retweet_tries = 0
document_count = 770001
formatted_tweets = 0

class MyListener(StreamListener):
    def __init__(self, api=None):
        super(MyListener, self).__init__()
        self.num_tweets = 0

    def writetodoc(self, json_formatted):
        global document_count
        global formatted_tweets
        formatted_tweets = open("./documents_crawl/formatted_tweets"+str(document_count)+".txt",'a',encoding='utf-8')
        formatted_tweets.write("Tweet ID                                     :"+json_formatted['id_str'] + "\n")
        tweet_keys = json_formatted.keys()
        try:
            for key in tweet_keys:
                #formatted_tweets.write("Text                   :"+json_formatted['text'] + "\n")
                key_string = str(key)
                if key_string == 'text':
                    formatted_tweets.write("\t\t*************TEXT*************\n")
                elif key_string == 'id_str' or key_string == 'id' or key_string == 'user' or key_string == 'entities':
                    pass
                else:
                    key_string_length = len(key_string)
                    spaces = key_indices_indendation - key_string_length
                    formatted_tweets.write(str(key))
                    while spaces > 0:
                        formatted_tweets.write(" ")
                        spaces -= 1
                my_value = json_formatted.get(key,"THIS_KEY_IS_ABSENT")
                if my_value == '0':
                    #formatted_tweets.write(str(key) +"                        :       THIS KEY HAS NO VALUE\n")
                    formatted_tweets.write(":       0\n")
                elif my_value == 'false':
                    formatted_tweets.write(":       false\n")
                elif my_value == "THIS_KEY_IS_ABSENT":
                    #formatted_tweets.write(str(key) +"                        :       EMPTY\n")
                    formatted_tweets.write(":       THIS_KEY_IS_ABSENT\n")
                else:
                    #formatted_tweets.write(str(key) +"                        :     "+ str(my_value)+"\n")
                    #my_value_str = str(my_value)
                    if key_string == 'text':
                        formatted_tweets.write(str(my_value) + "\n\n")
                    elif key_string == 'lang':
                        if str(my_value) == 'en':
                            formatted_tweets.write(":       "+ "ENGLISH" +"\n")
                        else:
                            formatted_tweets.write(":       "+ "NOT ENGLISH" +"\n")
                    elif key_string == 'id_str' or key_string == 'id':
                        pass
                    elif key_string == 'user':
                        for_user_inner_lists(my_value)
                        formatted_tweets.write("\n")
                    elif key_string == 'entities':
                        formatted_tweets.write("\n\n*******************ENTITIES INFORMATION*******************\n")
                        for_entities_inner_lists(my_value)
                        formatted_tweets.write("\n")
                    else:
                        formatted_tweets.write(":       "+ str(my_value) +"\n")
        except Exception as e:
            print("There is a write Error in doc no :\t" + str(document_count) + str(e))
            document_count += 1
            print("Occurred exception :" + str(e))
            return True
        formatted_tweets.write("\n")
        document_count += 1
        formatted_tweets.close()
        
    def on_data(self, data):
        global recursion_count
        global text_retweet_tries
        global document_count
        self.num_tweets += 1 
        try:
            with open('crawler_tweets.txt', 'a') as f:
                f.write(data)
                json_formatted = json.loads(data)
                if self.writetodoc(json_formatted):
                    self.num_tweets += 1
                tweet_keys = json_formatted.keys()
                for key in tweet_keys:
                    key_string = str(key)
                    my_value = json_formatted.get(key,"THIS_KEY_IS_ABSENT")
                    if my_value == '0' or my_value == 'false' or my_value == "THIS_KEY_IS_ABSENT":
                        pass
                    else:
                        if key_string == 'text' or key_string == 'retweeted_status':
                            text_retweet_tries += 1
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
                                        try:
                                            print("New word :" + word)
                                            word_dictionary[word] = words.count(word)
                                        except:
                                            print("New word is some integer")
                                            continue
                                else:
                                    pass
                        else:
                            pass
                if self.num_tweets > 12000:
                    recursion_count += 1
                    print("Recursion " + str(recursion_count) + " reached")
                    self.num_tweets = 0
                    twitter_stream.disconnect()
                    return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            pass
        return True
 
    def on_error(self, status):
        print(status)
        return True

frequent_tags = open('frequent_tags.txt', 'r')
frequent_terms = frequent_tags.read().splitlines()
filter_list = []

filter_list_size = 50
filter_count = 0

for term in frequent_terms:
    term = term.split(" ")
    word_dictionary[term[0]] = term[1]
    if filter_count < filter_list_size:
        filter_list.append(term[0])
        filter_count += 1
#print(filter_list)

'''   
#print("total_keys:" + str(count))     
#for key in word_dictionary.keys():
#    print(key, word_dictionary[key])
'''

def main():
    while recursion_count<2:
        twitter_stream = Stream(auth, MyListener())
        twitter_stream.filter(track=filter_list)
        print("Text/retweets that have been parsed : " + str(text_retweet_tries))
        filter_list.clear()
        filter_count = 0
        dict_size = 1
        for key in word_dictionary:
            word_dictionary[key] = int(word_dictionary[key])
            
        sorted_dictionary = sorted(word_dictionary, key = word_dictionary.get, reverse=True)
        # we will remove the top 50 every time from here, because we need to give chance to
        # to other tweets as well.
        
        for w in sorted_dictionary:
            if w in not_interested_words:
                continue
            else:
                filter_list.append(w)
                filter_count += 1
                print(w + ":" + str(word_dictionary[w]))
                if filter_count < filter_list_size:
                    continue
                else:
                    break_word = w
                    break
        reset_tags_count = filter_list_size
        
        #resetting the count of the top 500 frequent words to 501th word frequency 
        for w in sorted_dictionary:
            word_dictionary[w] = word_dictionary[break_word]
            reset_tags_count -= 1
            if reset_tags_count > 0:
                continue
            else:
                break

main()
