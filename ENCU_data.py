import requests
import os
import sys
from bs4 import BeautifulSoup
base_url = 'http://www.uefa.com'
url = 'http://www.uefa.com/uefaeuro/season=2016/teams/index.html'
country_url = 'http://www.uefa.com/uefaeuro/season=2016/teams/team=2/index.html'
def get_players(country_url):
    resp = requests.get(country_url)
    bsoup = BeautifulSoup(resp.content)
    team_wrap = bsoup.find('div', class_ = "squad--team-wrap")
    ul_tags = team_wrap.find_all('ul', class_ = 'squad--team-list')
    player_names = {}
    for ul_tag in ul_tags:
        for li_tag in ul_tag.find_all('li', class_ = 'squad--team-player'):
            player_name = li_tag.find('a')['title']
            player_role = li_tag.find('span', class_ = 'squad--player-role').text
            player_names.setdefault(player_role, []).append(player_name)
    return player_names

if __name__ == '__main__':

    fout = open('players', 'w')

    r = requests.get(url)
    print r.status_code
    print r.encoding
   # print r.content
    print type(r.content)
    r_content = BeautifulSoup(r.content)
    country_section = r_content.find_all('div', class_ = 'section--content clearfix')[0].find_all('div',class_ = 'row')[0:6]
    print len(country_section)
    cnt = 0
    for rows in country_section:
        #break
        divs = rows.find_all('div', class_ = 'col-md-6 col-lg-6 col-sm-6 col-xs-12 teams--qualified')
        for div in divs:
            country_url =  div.find('a', class_ = 'team-hub_link')['href']
            country = div.find('span', class_ = 'team-name_name').text
            target_url = ''.join((base_url, country_url))
            player_names = get_players(target_url)
            role_lines = [country]
            for role in player_names.keys():
                role_players = ','.join(player_names[role])
                role_lines.append(unicode(role_players))
                #print role_lines
            output_line = '#'.join(role_lines)
            fout.write(output_line.encode('utf-8') + '\n')
    fout.close()

    #get_players(country_url)
    print cnt
