import cgi

class tag_processor:

    def mask_tags(self, data):
        return cgi.escape(data)
    
    def del_tags(self, text):
        fixed_text = ''
        in_tag = False
        for letter in text:
            if letter == '<': in_tag = True
            if letter == '>':
                in_tag = False
                continue
            if in_tag: continue
            fixed_text += letter
        return fixed_text
    
    def prepare(self, text, tags = ['a', 'img', 'b', 'i']):
        
        prepared_text = text
        
        for tag in tags:
            topic_text = ""
            prepared_text = prepared_text.replace("&lt;/"+tag+"&gt;", "</"+tag+">").replace("&lt;"+tag+"", "<"+tag+" ")
            r_flag = False
            s_flag = 0
            
            for letter in prepared_text:
        
                if letter == '<':
                    r_flag = True
                    s_flag = 0
                          
                if r_flag:
                    if s_flag == 3:
                        if letter == ';':
                            s_flag = 0
                            r_flag = False
                            topic_text += '>'
                            continue
                        else: s_flag = 0
                    if s_flag == 2:
                        if letter == 't':
                            s_flag = 3
                        else: s_flag = 0
                    if s_flag == 1:
                        if letter == 'g':
                            s_flag = 2
                        else: s_flag = 0
                    if s_flag == 0:
                        if letter == '&':
                            s_flag = 1
                     
                if s_flag == 0: 
                    topic_text += letter
                
        return topic_text    
    
#t = tag_processor()
#text = """
#<a href="http://ya.ru">omg</a>
#<img src="qq.png"></img>
#"""
#print t.prepare(text)