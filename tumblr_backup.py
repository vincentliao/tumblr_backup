# Test tumblr client in Python
# tumblr API authentication: https://www.tumblr.com/oauth/apps

import pytumblr
import urllib
import urlparse
import os
import account
import re
import sys

class TumblrBackup:
    backup_folder = 'backup'
    def __init__(self):
        pass

    def folder_ready(self):
        if not os.path.exists(self.backup_folder):
            os.mkdir(self.backup_folder)

    def backup_current_state(self):
        ls_files = os.listdir(self.backup_folder)
        self.backup_ids = {}
        for filename in ls_files:
            matched = re.match(r'(\d+)_.*\.[a-z]+', filename)
            if matched:
                self.backup_ids[matched.group(1)] = filename

    def login(self):
        self.client = pytumblr.TumblrRestClient(**account.info['bakingcoding@gmail.com'])
        self.folder_ready()
        self.backup_current_state()

    def backup_all_likes(self):
        user_info = self.client.info()
        liked_posts_count = user_info['user']['likes']

        posts_per_package = 10
        for posts_offset in range(0, liked_posts_count, posts_per_package):
            liked_posts = self.client.likes(offset=posts_offset, limit=posts_per_package)
            for post_content in liked_posts['liked_posts']:
                if post_content['type'] == 'video':
                    self.download_video(post_content)
                elif post_content['type'] == 'photo':
                    self.download_photo(post_content)

    def download_file(self, post_id, url):
        if str(post_id) not in self.backup_ids:
            sr = urlparse.urlsplit(url)
            backup_filename = str.format('{folder}/{id}_{filename}', folder=self.backup_folder, id=post_id, filename=sr.path[sr.path.rfind('/')+1:])
            urllib.urlretrieve (url, backup_filename)
            print backup_filename
        else:
            print '.',
            sys.stdout.flush()

    def download_video(self, post_content):
        video_url = post_content.get('video_url')
        if video_url:
            self.download_file(post_content['id'], video_url)
        else:
            print 'video_url is None. post_id is ', post_content['id']

    def download_photo(self, post_content):
        for photo in post_content['photos']:
            photo_url = photo['original_size']['url']
            if photo_url:
                self.download_file(post_content['id'], photo_url)
            else:
                print 'photo_url is None. post_id is ', post_content['id']

if __name__ == '__main__':
    tb = TumblrBackup()
    tb.login()
    tb.backup_all_likes()
