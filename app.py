import streamlit as st
import time, nltk
import gender_guesser.detector as gender
from gradio_client import Client

class color:
   blue = '\033[96m'
   green = '\033[92m'
   yellow = '\033[93m'
   red = '\033[91m'
   end = '\033[0m'

def get_human_names(text):
	try:
		person_list = []
		tokens = nltk.tokenize.word_tokenize(text)
		pos = nltk.pos_tag(tokens)
		sentt = nltk.ne_chunk(pos, binary = False)
		person = []
		name = ""
		for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
			for leaf in subtree.leaves():
				person.append(leaf[0])
			if len(person) > 1: #avoid grabbing lone surnames
				for part in person:
					name += part + ' '
				if name[:-1] not in person_list:
					person_list.append(name[:-1])
				name = ''
			person = []
	except LookupError:
		print(f'{c.yellow}Downloading nltk stuff (one time only)...{c.blue}')
		nltk.download('punkt')
		nltk.download('averaged_perceptron_tagger')
		nltk.download('maxent_ne_chunker')
		nltk.download('words')
		nltk.download('omw-1.4')
		person_list = get_human_names(text)
	return [x for x in person_list if x not in ('Shen Yun')]

def guess_gender(name):
    gender = get_gender_guesser().get_gender(name.split(' ')[0])
    possible_genders = {
        'male':'(Man)',
        'female':'(Woman)'
    }
    return possible_genders.get(gender,'(Man)')

@st.cache_resource
def get_gender_guesser():
    return gender.Detector()

def main():
    uploaded_file = st.file_uploader("Upload Audio", type=["mp3", "m4a", "wav", "wma"])
    if uploaded_file:
        with open("uploads", "wb") as f:
            f.write(uploaded_file.getbuffer())
        with st.spinner('Waiting for whisperjax API...'):
            client = Client("https://sanchit-gandhi-whisper-jax.hf.space/")
            text, runtime = client.predict('uploads',"transcribe",False,api_name="/predict_1")
        text=text[1:] #remove space in beginning

        #Make common corrections
        corrections = {
            'Falengon':'Falun Gong',
            'Shenmue':'Shen Yun',
            'Ximing':'Shen Yun',
            'Shen Ying':'Shen Yun',
            'Dava':'Dafa',
            'I pick Times':'Epoch Times',
            'Epic Times':'Epoch Times'
        }
        for x in corrections:
            text = text.replace(x,corrections[x])

        names = {x:guess_gender(x) for x in get_human_names(text)}
        initial = next(iter(names))[0]+': ' if len(names) else ': '

        #Split into Question-Answer format
        b = text.replace('? ','?\n').replace('! ','!\n').split('\n')
        c = [b for a in (x.replace('. ','.\n').split('\n') for x in b) for b in a]
        d = [c[i].upper() + ('\n'+initial if c[i].endswith('?') and (i + 1 < len(c) and not c[i + 1].endswith('?')) else ' ') if c[i].endswith('?') else c[i] + ('\n\n' if c[i].endswith(('.','!')) and (i + 1 < len(c) and c[i + 1].endswith('?')) else ' ') if c[i].endswith(('.','!')) else c[i] for i in range(len(c))]
        text = ''.join(d)

        text = '\n'.join(tuple(f'{x[0]}: {x} {names[x]}, ' for x in names))+'\n\n'+text

        text = uploaded_file.name+'\nTranscriber: Michael Chen\n\n'+text

        st.text_area(label='transcript',value=text,height=600,label_visibility='hidden')

if __name__ == "__main__":
    main()
