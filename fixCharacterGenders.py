def tolower(s):
    return s.lower()

if __name__ == "__main__":
    
    with open('data/name-gender/female.txt') as f:
        fnames = list(map(tolower, f.read().split('\n')))
    
    with open('data/name-gender/male.txt') as f:
        mnames = list(map(tolower, f.read().split('\n')))

    with open('data/cornell movie-dialogs corpus/movie_characters_metadata.txt', 
        encoding='ISO-8859-1') as f:
        cdb = f.read().split('\n')
    
    cdb_clean = []
    count = 0
    for cinfo in cdb:
        cinfo = cinfo.split(' +++$+++ ')
        try:
            if cinfo[-2] == '?':
                b1 = cinfo[1].lower() in fnames
                b2 = cinfo[1].lower() in mnames
                if b1 != b2:
                    count += 1
                    if b1:
                        cinfo[-2] = 'f'
                    else:
                        cinfo[-2] = 'm'
            cdb_clean.append(' +++$+++ '.join(cinfo))
        except:
            pass    

    s = '\n'.join(cdb_clean)

    with open('data/cornell movie-dialogs corpus/movie_characters_metadata.txt', 'w') as f:
        f.write(s)

    print("{} genders fixed from name-gender list".format(count))
