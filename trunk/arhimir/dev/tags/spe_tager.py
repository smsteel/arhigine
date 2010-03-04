import operator
import random
 
#this is a tag cloud script-generator created by spe
class Tager:
 
#    #just a piece of cloud!
#    class Tag:
#        def __init__(self, name, size):
#            self.name=name
#            self.size=size
#    
    #constructor
    def __init__(self):
        self.clouds = []
 
    def get_html_clouds(self, tags):      
        clouds=[]
        tags.sort(cmp=None, key=None, reverse=False)
 
        old_tag = tags[0]
        cloud_size = 0
        for tag in tags:
            if tag != old_tag:
                #t_tag = self.Tag(old_tag, cloud_size)
                clouds.append((old_tag, cloud_size))
                old_tag = tag
                cloud_size = 0
            else: cloud_size += 1
 
        returner = ""
        cnt = 0
        for cloud in sorted(clouds, key=operator.itemgetter(1), reverse=True):
            if cloud[0]=="": continue
            try:
                if cnt==0: self.clouds.append("<span style='cursor: pointer; font-size: 38px;' onclick='search(\"" + cloud[0] + "\");'><font color='#48478D'>"+cloud[0]+" </font></span>")
                elif cnt<=2: self.clouds.append("<span style='cursor: pointer; font-size: 32px;' onclick='search(\"" + cloud[0]  + "\");'><font color='#48478D'>"+cloud[0]+" </font></span>")
                elif cnt<=5: self.clouds.append("<span style='cursor: pointer; font-size: 26px;' onclick='search(\"" + cloud[0]  + "\");'><font color='#48478D'>"+cloud[0]+" </font></span>")
                elif cnt<=9: self.clouds.append("<span style='cursor: pointer; font-size: 20px;' onclick='search(\"" + cloud[0] + "\");'><font color='#48478D'>"+cloud[0]+" </font></span>")
                elif cnt<=14: self.clouds.append("<span style='cursor: pointer; font-size: 18px;' onclick='search(\"" + cloud[0]  + "\");'><font color='#48478D'>"+cloud[0]+" </font></span>")
                elif cnt<=20: self.clouds.append("<span style='cursor: pointer; font-size: 16px;' onclick='search(\"" + cloud[0]  + "\");'><font color='#48478D'>"+cloud[0]+" </font></span>")
                elif cnt<=27: self.clouds.append("<span style='cursor: pointer; font-size: 14px;' onclick='search(\"" + cloud[0]  + "\");'><font color='#48478D'>"+cloud[0]+" </font></span>")
            except:pass
            cnt+=1
 
        random.shuffle(self.clouds)
 
        #return "<font style='cursor: pointer;' onclick='search(this);' size=7>"+"</font>&nbsp;"
 
        for cloud in self.clouds:
            returner+=cloud
        return '<div style="width: 300px; margin-top: 150px; text-align: center; padding: 5px;"><form id="tag_search" action="/search/" method="post"><input id="tag_search_val" type="hidden" name="find" value="" /></form>'+returner+'</div>'
 
 
 
