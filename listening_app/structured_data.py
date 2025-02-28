# Create a prompt that instructs the LLM to extract the questions.
from chat import DeepSeekChat


transcript = """"
hi guys welcome to another series this
is going to be a tutorial about basic
Japanese words and grammar based from
the monotony hunger textbook this is for
the absolute beginners or for those who
want to review their Japanese this is
also the textbook I use when I first
start learning
nihongo a long time ago although I am
not yet 100% fluent I can speak and
communicate using basic Japanese I only
attended Japanese language school for
about three months so pretty much I've
learned Japanese or nihongo through
self-study and getting used to talking
and listening to Japanese at work like I
said if you are an absolute beginner who
is interested in learning nihongo I hope
you find this tutorial helpful also I'm
from the Philippines so you might hear
me say Tagalog or Filipino words once in
a while so don't be surprised solid ever
had him in my shop that's Japanese for
let's begin
this is Minna no nihongo lesson 1
vocabulary what she what does she other
words to say what a she our array or
boku which men generally use another
word is a tushy used by females to sound
more feminine or cute and the very
formal way of saying what she is
watashi which you will hear usually in a
very formal setting or situation what -
it touchy what are touchy ah na anata i
noticed that when you're not very close
to someone you're talking to you don't
address them directly as anata or you
but instead you call them or address
them by their name so for example you
wanna ask are you okay directly to the
person you're talking to you say for
example that their name
um suzuki-san so you say is that uh are
you Anna tawa daijoubu desu ka' you say
Suzuki Samurai Java deskah are you ok
mr. Suzuki so just be very careful with
using anata again if you're not very
close to someone it's better to use or
adjust them by their first name or last
name followed by Sun instead of saying
anata also this word can also be used as
a term of endearment sometimes wives
would refer or call their husband
anata uh no hito a no hito or the more
polite way of saying this is f no kata
anakata I know means that and he top
means person me nah son Mina Sun Sun Sun
so this is the equivalent of mr. miss or
mrs. in English and it's just a way of
showing respect to the person you're
talking to
chan Chan in general it is used for
babies for example Akutan or research
and or young children or even
grandparents like oppa Chan or GTM but
this can also be used among friends or
lovers who've known each other for a
long time this this means that the
speaker finds the other person cute or
attractive or lovable kun kun in general
it is used for young boys or young adult
male or even among male friends Jin Jin
for example a Filipino is Philippine
Jean an American is America Jean and a
Japanese person is me hyung Jin and so
on sensei sensei notice that we have a
long vowel
at the end say okay
sensei Yoshi cure again another
long vowel cure your sheep so the
difference between sensei
and Kyo she is that sensei is only
referring to another teacher so if you
are going to introduce yourself and you
wanna say that you you are a teacher you
say watashi wa Yoshi this Gakusei tuxie
notice how we how we don't pronounce the
you in the cook syllable it becomes duck
say Chi sha in Tai Shan Tai Chi Minh's
company and in means member sha in shine
ginkgo in ginkgo in notice that the N
syllable or not becomes ng sound because
it is followed by a K or Co so it
becomes gingko gingko in gingko means
bank and in again means member yah yah
cane fuchsia tank Usha and Jimmy
engineer died could die duck be all in
be Owen danke
thank you
da-rae daddy or the more polite way is
donut donut ah sigh sigh for example
five years old is go sigh and thirty
years old is son Josiah none sigh none
sigh or the more polite way is I could I
could sit hi hi yeah II so make sure
that you extend the ISA Level II yeah
she today this guy today this guy or
sits today this nut so the syllable can
also be pronounced as not so whether you
pronounce it as a gap or ax is just a
personal preference today this guy stood
a the singer oh na ma Iowa or Nam Iowa
so the translation is may I have your
name
but this literally means your name is
with a rising intonation this is a
casual or informal way of asking
someone's name now ma a is a Japanese
boy name and the prefix o makes it more
polite but if you are in a formal
setting it is best to say anima wa nan
desu ka' which means what's your name
Hajime mashite a Hajime mistake so this
is the first phrase or an expression
that you say when you're introducing
yourself for the first time to someone
it means how do you do but it it's the
literal translation is for the first
time so usually it goes like how do you
manage their watashi wa daddy that it is
so notice that the I in the sheet
syllables become silent
has he me mash them those Oh yoroshiku
onegaishimasu the natural way of saying
this is those are your Ascona kazuma's
so this is a very formal expression
usually used at the end of a
self-introduction a less formal way of
saying this is those Orozco
orgeous yashka this phrase actually has
other meanings depending on the
situation which you will learn later on
but for the meantime this means pleased
to meet you or please be nice to me
kochira wa daddy that I sang this so
that idea is who so I just replaced the
the back part with daddy daddy
so meaning you put in a name of someone
there so this phrase is used when you
are introducing someone someone else

"""

prompt = f"""
You are given a transcript of a JLPT listening practice test. Please extract each question and organize it into a JSON array. 
Each question object should have exactly three keys:
- "introduction": Any introductory text before the main conversation.
- "conversation": The dialogue or conversation section.
- "question": The actual question being asked.

Ensure that the output is valid JSON and contains only the JSON array without any additional commentary.
Transcript:
{transcript}
"""

# Initialize the LLM wrapper
chat = DeepSeekChat()

# Generate the response
response = chat.generate_response(prompt)

print(response)