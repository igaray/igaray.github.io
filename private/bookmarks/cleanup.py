#!/usr/bin/env python3
import time
import urllib.request
import urllib.error
import bs4

filenames = [
  "bm.yaml",
  "bm_cs_ai.yaml",
  "bm_cs_algorithms.yaml",
  "bm_cs_excellency.yaml",
  "bm_cs_pl.yaml",
  "bm_cs_plt.yaml",
  "bm_cs_tools.yaml",
  "bm_cs_topics.yaml",
  "bm_humanities.yaml",
  "bm_mind.yaml",
  "bm_videos.yaml"
  ]

def strip_protocol(line):
  if line.startswith("- https://"):
    return line[13:]
  elif line.startswith("- http://"):
    return line[12:]
  else:
    return line

def gather(filename):
  with open(filename, "r") as bm:
    for line in bm:
      bm_set.add(strip_protocol(line))

def is_bookmark(line):
    return "- [ ] http" == line[:10]

def get_url(line):
    return line[6:-1]

def get_title(url):
    code = 0
    title = url
    try:
        with urllib.request.urlopen(url) as response:
            code = response.getcode()
            html = response.read()
            soup = bs4.BeautifulSoup(html, 'html.parser')
            if soup.title:
                title = soup.title.string
            title = title.replace('\n', ' ').strip()
    except urllib.error.HTTPError as error:
        code = error.code
        title = None
    except urllib.error.URLError as error:
        title = None
    except Exception as error:
        title = None
    return (code, title)

def main():
    # DEDUP
    bm_set = set()
    for filename in filenames:
      gather(filename)

    with open("bm_unsorted.org", "r") as bm_unsorted:
      with open("bm_unsorted_dedup.org", "w") as bm_dedup:
        for line in bm_unsorted:
          if strip_protocol(line) not in bm_set:
            bm_set.add(strip_protocol(line))
            bm_dedup.write(line)

    # TITLES
    with open("bm_unsorted.org", "r") as input_file:
        with open("titles.org", "w") as output_file:
            i = 1
            for line in input_file:
                if is_bookmark(line):
                    url = get_url(line)
                    code, title = get_title(url)
                    print("\r{0:>5} {1:>3} {2}".format(i, code, url))
                    if title:
                        output_file.write("- [ ] [[{0}][{1}]]\n".format(url, title))
                    else:
                        output_file.write(line)
                else:
                    output_file.write(line)
                i += 1

if __name__ == "__main__":
    main()
