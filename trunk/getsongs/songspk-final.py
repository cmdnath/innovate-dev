"""
@author : Dharmendra Kumar Verma
"""

from sgmllib import SGMLParser
import urllib
import urllib2
import sys
import os
import collections
os.system("cls && echo WELCOME ...  ")  # Helps in clsing console and greeting the user
try:
    import eyed3

    """
    eyeD3 is a Python tool for working with audio files, specifically mp3 files containing ID3 metadata (i.e. song info).
    To Read More Please visit - http://eyed3.nicfit.net/

    """
except:
    os.system('cls && echo PLEASE WAIT ...')
    print """eyed3 in not installed, Songs title will not be renamed properly, or some songs overwrite problem may occur\n
                To install you can exit the script and then type \n
                \t\t 'sudo pip install eyed3'
    """
    user_in = raw_input("Enter 'yes' to continue or 'no' to exit\n")
    if user_in.lower() != 'yes':
        sys.exit(0)


class URLLister(SGMLParser):
    """
    SGMLParser which serves as the basis for parsing text files formatted in SGML (Standard Generalized Mark-up Language).
    Infact, it does not provide a full SGML parser it only parses SGML insofar as it is used by HTML, and the module only
    exists as a base for the htmllib module. Another HTML parser which supports XHTML and offers a somewhat different interface
    is available in the HTMLParser module.

    SGMLParser.reset()
        Reset the instance. Loses all unprocessed data. This is called implicitly at instantiation time.


    reset method overrided

    """
    def reset(self):
        SGMLParser.reset(self)
        self.urls = []

    def start_a(self, attrs):
        href = [v for k, v in attrs if k == 'href']
        if href:
            self.urls.extend(href)


class SongsPK():

    VERSION = 1.1
    #Default directory path on your Desktop
    DIRPATH = os.path.expanduser('~/Desktop/songsPK_Collection')

    def __init__(self):
        """
        checks the existence of default output directory , If not present it will create.
        As default location is set to user Desktop, program is not checking the write permission of directory.
        If directory error please check the write permission of user of ~/Desktop .

        """
        if not os.path.exists(self.DIRPATH):
            os.mkdir(self.DIRPATH)
        while True:
            print "Please select an option to proceed\n"
            print "1 - Url based bulk song download\n"
            print "2 - Movie name based bulk song download\n"
            print "3 - Exit\n"
            try:
                option = input('Enter your option {1 or 2}\n')
                os.system('cls')
            except Exception as e:
                    print e.message  # To display the error message in console
                    continue
            if option == 1:
                self.urlbased()
                os.system('cls')
                continue
            elif option == 2:
                self.moviehandler()
                os.system('cls')
                continue
            elif option == 3:
                break
            else:
                print "Invalid option"
                continue
        os.system('cls && echo PLEASE WAIT ...')
        
    def url_opener(self, url_data):
        """
        Common function for  getting url_data from a passed url and return the object of class URLLister(SGMLParser)

        """

        user_agent = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; InfoPath.3)'
        req = urllib2.Request(url_data)
        req.add_header('User-Agent', user_agent)

        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        parser = URLLister()
        parser.feed(link)
        parser.close()
        return parser

    def write_mp3(self, mp3):
        """
        Writes the downloaded file and renames the title.

        """
        name = (mp3.geturl()).split('/')
        folder_name = os.path.expanduser(self.DIRPATH+'/'+name[-2]+'/')
        song_name = name[-1]
        song_name = urllib2.unquote(song_name)

        if not os.path.exists(folder_name):
            os.mkdir(folder_name) # Creates a directory on current users Desktop
        #File Opening and writing
        fullpath = folder_name+song_name

        u = urllib2.urlopen(mp3.geturl())
        f = open(fullpath, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (fullpath, file_size)

        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            f.write(buffer)
        f.close()
        """
        try:
            audiofile = eyed3.load(fullpath)  # eyed3 module used for changing the audio file properties.
            if audiofile.tag.title:
                os.rename(fullpath, folder_name+audiofile.tag.title) # Renaming the downloaded file title
        except:
            print "Not able to edit title"
            pass
        """

    def urlbased(self, url_datas=None):
        """
        Prepares the url and then download the mp3 file. To write the file in Disk it depends on write_mp3 function
        """
        visited_url = []
        if not url_datas:
            url_datas = raw_input("Enter comma separated url strings\n")
            os.system('cls && echo PLEASE WAIT ...')
        url_datas = url_datas.split(',')
        url_count = 0
        for url_data in url_datas:
            if url_data.startswith('www'):
                url_data = url_data.replace('www', 'http://www')
            parser = self.url_opener(url_data)
            url_count += 1
            parse_url = 0
            for url in parser.urls:
                parse_url += 1
                try:
                    user_agent = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; InfoPath.3)'
                    req = urllib2.Request(url)
                    req.add_header('User-Agent', user_agent)
                    res = urllib2.urlopen(req)  # Resolve the redirects and gets the song Object
                    finalurl = res.geturl()
                    # Now check the function
                    if finalurl.endswith('.mp3') and finalurl not in visited_url and not finalurl.startswith('..'):
                        self.write_mp3(res)  # call to write mp3 file in Disk
                    visited_url.append(finalurl)
                except Exception as e:
                    #print e.args
                    continue
                #print str(int(parse_url*100)/len(parser.urls)) + "percent songs processed of url --->" + str(url_count)

    def moviehandler(self):

        """
            Get Movie name list and allow user to enter multiple movie number to download songs from all the movies in one hit.

            STEPS- Enter starting letter of any indian Movie
                   Select your movie number from the displayed list
                   Files will be downloaded on your desktop in a folder named songsPK_Collection.Movie Name
            os command mainly has been used for clsing the mess

        """
        movie_letter = raw_input('Enter Indian Movie start letter [A-Z] to get movie name list\n')
        os.system('cls && echo PLEASE WAIT ...')
        url_data = "http://songspk.info/indian_movie/%s_List.html" % movie_letter.upper()
        parser = self.url_opener(url_data)
        surl_dict = {}
        url_dict = {}
        count = 1
        for url in parser.urls:
            if not url.startswith('..'):
                url_dict[str(count)] = url
                surl_dict[url] = str(count)
                count += 1
        surl_dict = collections.OrderedDict(sorted(surl_dict.items()))
        for k, v in surl_dict.iteritems():
            print v.rjust(4) + '-----' + k.rstrip('.html')

        movie = raw_input('Enter comma separated movie number to download all songs of movies\n')
        movie = movie.split(',')
        os.system('cls && echo PLEASE WAIT ...')
        movie_url = ''
        for no in movie:
            movie_url += "http://songspk.info/indian_movie/%s" % url_dict[no] + ','
        movie_url = movie_url.rstrip(',')
        self.urlbased(url_datas=movie_url)

if __name__ == "__main__":
    SongsPK()
