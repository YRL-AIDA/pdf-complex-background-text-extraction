import glob
# -*- coding: utf-8 -*-
import requests
from font_recognition import FontRecognizer

data = {
    "document_type": "other",
    "language": "rus+eng",
    "need_pdf_table_analysis": "true",
    "need_header_footer_analysis": "false",
    "is_one_column_document": "true",
    "return_format": 'plain_text',
    "structure_type": 'tree',
    'pages': '1:1',
    'pdf_with_text_layer': 'false'
}

q = "../data/checkpdf2"
qq = "../data/checkpdf"
norm = [f'{q}/152.pdf', f'{q}/069.pdf', f'{q}/089.pdf', f'{q}/154.pdf', f'{qq}/mongolo.pdf']
pdf = norm[3]
with open(pdf, 'rb') as file:
    files = {'file': (pdf, file)}
    r = requests.post("http://localhost:1231/upload", files=files, data=data)
    result = r.content.decode('utf-8')
    dedoc_text = ' '.join(result.split())
    print(dedoc_text)
# pdfs = glob.glob("../data/pdf/*.pdf")
# fr_re = FontRecognizer.load_default_model()
# for pdf in pdfs:
#     print(pdf)
#     with open(pdf, 'rb') as file:
#         files = {'file': (pdf, file)}
#         r = requests.post("http://localhost:1231/upload", files=files, data=data)
#         result = r.content.decode('utf-8')
#         # print(' '.join(result.split()))
#         tabby_text = ' '.join(result.split())
#     print(tabby_text)
#     print('=============')

# ../data/pdf\double_lines.pdf
# University of South Carolina Scholar Commons Theses and Dissertations 1-1-2013 Some Assembly Required Anthony Feggans University of South Carolina Follow this and additional works at: https://scholarcommons.sc.edu/etd Part of the Creative Writing Commons Recommended Citation Feggans, A.(2013). Some Assembly Required. (Master's thesis). Retrieved from https://scholarcommons.sc.edu/etd/2316 This Open Access Thesis is brought to you by Scholar Commons. It has been accepted for inclusion in Theses and Dissertations by an authorized administrator of Scholar Commons. For more information, please contact digres@mailbox.sc.edu.
# =============
# ../data/pdf\mongolo.pdf

# =============
# ../data/pdf\pdf1.pdf
# See discussions, stats, and author profiles for this publication at: https://www.researchgate.net/publication/330984977 Pregnancy with successful foetal and maternal outcome in a melanoma patient treated with nivolumab in the ﬁrst trimester: case report and review of the literature Article in Melanoma Research · February 2019 DOI: 10.1097/CMR.0000000000000586 CITATIONS 55 READS 299 4 authors, including: Wen Xu Princess Alexandra Hospital (Queensland Health) 61 PUBLICATIONS 793 CITATIONS SEE PROFILE Victoria Atkinson Princess Alexandra Hospital (Queensland Health) 174 PUBLICATIONS 18,042 CITATIONS SEE PROFILE All content following this page was uploaded by Wen Xu on 24 August 2020. The user has requested enhancement of the downloaded file.
# =============
# ../data/pdf\pdf2.pdf
# Как познакомиться с помощью Шаблона Стагнера? Прежде всего необходимо избавиться от иллюзии, что каждая красотка в баре просто стерва, которая ищет себе исключительно богатых мужиков... Это очень ограниченное убеждение и, более того, оно в принципе неверно. Представьте себя такой красоткой, которая пришла просто отдохнуть. Целая куча пьяного быдла в три раза крупнее вас станет добиваться вашего внимания и секса.
# =============
# ../data/pdf\pdf3.pdf
# 213 Folia Zool. – 54(1–2): 213–216 (2005) Diet composition of red fox during rearing in a moor: a case study József LANSZKI University of Kaposvár, Faculty of Animal Science, Ecological Research Group, P .O. Box 16, H-7401 Kaposvár, Hungary; e-mail: lanszki@mail.atk.u-kaposvar.hu Received 11 October 2004; Accepted 23 May 2005 A b s t r a c t . The diet of red fox (Vulpes vulpes) cubs living in a moor in Hungary was studied by scat analysis (n = 77) during the rearing period. The main food source of foxes consisted of small mammals (preferred Microtus voles) which was supplemented with brown hare and gamebirds rarely. Cubs ate remains of carrions (domestic animals, ungulates and carnivores) and invertebrates frequently but in low quantity. The food consisted of characteristically terrestrial, occasionally aquatic and rarely arboreal prey. Vulpes vulpes, cubs, Microtus preference, Hungary Key words: Introduction Red fox Vulpes vulpes (L.) is a generalist predator, widely spread and common species in Europe (L l o y d 1980). In Hungary, the red fox population has increased in recent years (in 1988: 4.9 ind./1000 ha, in 2001: 12.8 ind./1000 ha, H e l t a i 2002). The diet in spring and summer is primarily composed of small mammals, and in addition to these, also birds, hare, fruits and carrion are important e.g. on meadows, woods and agricultural landscapes in central Europe (S u c h e n t r u n k 1984, G o s z c z y n s k i 1986, K o ž e n á 1988, J e d r z e j e w s k a & J e d r z e j e w s k i 1998). Compared to other habitats, the feeding habits of fox in the shrinking moor areas (L e c k i e et al. 1998), especially in the Pannonian region are less known. Moreover, the qualitative and quantitative characteristics of the food that the vixen supply the cubs with (K o l b & H e w s o n 1980, L l o y d 1980) are also described to a lesser extent. The aim of this case study was to investigate the diet and feeding habits of red fox living in a moor during the cubs’ dependency stage. Material and Methods The study area, named Nagybereki Fehérvíz Moor Nature Conservation Area is situated in western Hungary (46°38’ N, 17°32’ E, 99m a.s.l.). The typical vegetations of this area are mire willow scrubs (Salicetum spp.), large sedge communities (Carex spp.) and alder swamp wood (Cariceti elongatae-Alnetum). A rich fen is located on the area, which is periodically used as cow pasture. The diet of the red fox were studied by scat analysis. Samples (n = 77) were collected between 14 April 2002 to 18 July 2002 around a fox den. Prey determination was performed by microscope on the basis of feather, bone, dentition and hair characteristics (more detail: L a n s z k i 2003). Diet composition was expressed as the relative frequency of occurrence and as an estimate of the percentage fresh weight (biomass) of food consumed (J e d r z e j e w s k a & J e d r z e j e w s k i 1998). Survey of the small mammal food N O T E
# =============
# ../data/pdf\type1.pdf
# Notes on reading Adobe font ﬁles by Bill Casselman Adobe Type 1 font ﬁles are special types of PostScript ﬁles which are read by their own special PostScript interpreter. There are two major parts to one of these, the ﬁrst containing the character encoding and the second the character descriptions . In practice, these ﬁles almost always come with two extensions, .pfa and .pfb. The major difference between these two is that a certain part of the font speciﬁcation, known as the binary section , is stored as raw bytes in .pfb ﬁles, but as bytes in the form of pairs of hex characters in .pfa ﬁles. Most fonts are stored on a system in .pfb format because these ﬁles are about half the size of the equivalent .pfa ﬁle, but using a Type 1 font in a PostScript program requires translation to the longer .pfa format before importing it. There are several reasons why one might wish to analyze one of them: • convert a .pfb ﬁle to a .pfa ﬁle in order to load the font into a PostScript program; • extract from one of them the references to only a subset of characters in order to include the shortened font in a PostScript program; • extract character path descriptions to use in a graphics program that is not necessarily PostScript. All three of these are relevant to me, since my graphics program PiScript does a lot of manipulation of Type 1 fonts. My principal references for this note have been Adobe’s manual for Type 1 Fonts, and the source code for the t1utils package (look at the discussion at the end of this note). 1. The basic structure A Type 1 font ﬁle has three segments. In order: (a) an initial ascii part (b) the middle part (c) a ﬁnal ascii part Parts (a) and (c) are always in printable ascii characters, but the middle part (b), which is basically in a binary format, differs in.pfa and .pfb ﬁles. In the .pfb format the data in this middle section is stored as raw bytes, whereas in the .pfa version these bytes are stored in hexadecimal ascii format. Since raw bytes are not so amenable to parsing, .pfb ﬁles have in addition certain segment headers which specify the lengths of segments in the ﬁle. There are four of these. The binary sections in all Type 1 font ﬁles contain the instructions for actually drawing the characters of the font. The entire Type 1 ﬁle is created from an original ascii ﬁle by two or possibly three stages of encryption. Two of these are open—i.e. the algorithms for encryption and decryption have been published by Adobe Systems. It is not clear to me what the purpose of these top levels of encryption is. A document by Adobe says that they discourage casual inspection, but it is not hard to write a program that deciphers them. I am not aware that fonts are enciphered in a truly secret manner. Certainly many publicly available fonts, in particular all those derived from Donald Knuth’s original cm fonts, are completely readable. It is extremely easy to convert back and forth between .pfb and .pfa format. A .pfb ﬁle is not easy to parse, so it contains three segment headers to help navigate. Each begins with a binary segment header of 6 bytes. The ﬁrst byte is always the hex form 80 of 128. The second tells the type of the header, which is 1 for the initial header. The next four bytes specify the length of the ﬁrst ascii segment, in low­endian order. Thus the initial segment header of cmr10.pfb is (in decimal notation) 128:1:27:14:0:0, which tells that the length of the ﬁrst segment is 27 + 14 · 256 = 3611 characters. What this means is that the next header is byte number 6 + 3611 = 3617 of the ﬁle, and that bytes in the range [6, 3617)make up the initial ascii segment. Similarly, there are two more segment headers in the ﬁle, each one starting just at the end of the segment marked by the previous one. There is one ﬁnal last ‘header’ of two bytes, always [128 : 3], which functions as an end­of­ﬁle marker. It is presumably there to ﬂag ﬁle corruption. 1
# =============
