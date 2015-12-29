
#Fivebit version 0.2b [27/11/2014] by Dankoozie

#In this version we substitute dictionary values after the main substitute function has completed

#5bit encoding / compression
#0-25 - abcdefghijklmnopqrstuvwxyz
#26 - Spás
#27 - Change to UCase
#   - 27,31 Caps lock on
#   - 27,30 Num lock on
#   - 27,31...31 release


#28 - Numeric/Punc.  
#29 - Reserved
#30 - Dict1024
#31 - UTF-8 escape

from math import ceil
#from struct import unpack

std_chars = {0:'a', 1: 'b',2: 'c',3: 'd',4: 'e',5: 'f',6: 'g',7: 'h',8: 'i',9: 'j',10: 'k',11: 'l',12: 'm',13: 'n',14: 'o',15: 'p',16: 'q',17: 'r',18: 's',19: 't',20: 'u',21: 'v',22: 'w',23: 'x',24: 'y',25: 'z', 26: ' '} 

std_ucase = {0:'A', 1: 'B',2: 'C',3: 'D',4: 'E',5: 'F',6: 'G',7: 'H',8: 'I',9: 'J',10: 'K',11: 'L',12: 'M',13: 'N',14: 'O',15: 'P',16: 'Q',17: 'R',18: 'S',19: 'T',20: 'U',21: 'V',22: 'W',23: 'X',24: 'Y',25: 'Z', 26: ' '}

std_chars_decode = ((0,'a'),(0,'b'),(0,'c'),(0,'d'),(0,'e'),(0,'f'),(0,'g'),(0,'h'),(0,'i'),(0,'j'),(0,'k'),(0,'l'),(0,'m'),(0,'n'),(0,'o'),(0,'p'),(0,'q'),(0,'r'),(0,'s'),(0,'t'),(0,'u'),(0,'v'),(0,'w'),(0,'x'),(0,'y'),(0,'z'),(0,' '),(1,''),(2,''),(3,''),(4,''),(5,''))

num_chars = {32: [26], 33: [28, 0], 34: [28, 1], 35: [28, 2], 36: [28, 3], 37: [28, 4], 38: [28, 5], 39: [28, 6], 40: [28, 7], 41: [28, 8], 42: [28, 9], 43: [28, 10], 44: [28, 11], 45: [28, 12], 46: [28, 13], 47: [28, 14], 48: [28, 15], 49: [28, 16], 50: [28, 17], 51: [28, 18], 52: [28, 19], 53: [28, 20], 54: [28, 21], 55: [28, 22], 56: [28, 23], 57: [28, 24], 58: [28, 25], 59: [28, 26], 60: [28, 27], 61: [28, 28], 62: [28, 29], 63: [28, 30],64: [28, 31]}

dic1024 = {0: 'the', 1: 'and', 2: 'have', 3: 'that', 4: 'for', 5: 'you', 6: 'with', 7: 'say', 8: 'this', 9: 'they', 10: 'but', 11: 'his', 12: 'from', 13: 'not', 14: 'she', 15: 'what', 16: 'their', 17: 'can', 18: 'who', 19: 'get', 20: 'would', 21: 'her', 22: 'all', 23: 'make', 24: 'about', 25: 'know', 26: 'will', 27: 'one', 28: 'time', 29: 'there', 30: 'year', 31: 'think', 32: 'when', 33: 'which', 34: 'them', 35: 'some', 36: 'people', 37: 'take', 38: 'out', 39: 'into', 40: 'just', 41: 'see', 42: 'him', 43: 'your', 44: 'come', 45: 'could', 46: 'now', 47: 'than', 48: 'like', 49: 'other', 50: 'how', 51: 'then', 52: 'its', 53: 'our', 54: 'more', 55: 'these', 56: 'want', 57: 'way', 58: 'look', 59: 'first', 60: 'also', 61: 'new', 62: 'because', 63: 'day', 64: 'use', 65: 'man', 66: 'find', 67: 'here', 68: 'thing', 69: 'give', 70: 'many', 71: 'well', 72: 'only', 73: 'those', 74: 'tell', 75: 'very', 76: 'even', 77: 'back', 78: 'any', 79: 'good', 80: 'woman', 81: 'through', 82: 'life', 83: 'child', 84: 'work', 85: 'down', 86: 'may', 87: 'after', 88: 'should', 89: 'call', 90: 'world', 91: 'over', 92: 'school', 93: 'still', 94: 'try', 95: 'last', 96: 'ask', 97: 'need', 98: 'too', 99: 'feel', 100: 'state', 101: 'never', 102: 'become', 103: 'between', 104: 'high', 105: 'really', 106: 'something', 107: 'most', 108: 'another', 109: 'much', 110: 'family', 111: 'own', 112: 'leave', 113: 'put', 114: 'old', 115: 'while', 116: 'mean', 117: 'keep', 118: 'student', 119: 'why', 120: 'let', 121: 'great', 122: 'same', 123: 'big', 124: 'group', 125: 'begin', 126: 'seem', 127: 'country', 128: 'help', 129: 'talk', 130: 'where', 131: 'turn', 132: 'problem', 133: 'every', 134: 'start', 135: 'hand', 136: 'might', 137: 'show', 138: 'part', 139: 'against', 140: 'place', 141: 'such', 142: 'again', 143: 'few', 144: 'case', 145: 'week', 146: 'company', 147: 'system', 148: 'each', 149: 'right', 150: 'program', 151: 'hear', 152: 'question', 153: 'during', 154: 'play', 155: 'government', 156: 'run', 157: 'small', 158: 'number', 159: 'off', 160: 'always', 161: 'move', 162: 'night', 163: 'live', 164: 'point', 165: 'believe', 166: 'hold', 167: 'today', 168: 'bring', 169: 'happen', 170: 'next', 171: 'without', 172: 'before', 173: 'large', 174: 'must', 175: 'home', 176: 'under', 177: 'water', 178: 'room', 179: 'write', 180: 'mother', 181: 'area', 182: 'national', 183: 'money', 184: 'story', 185: 'young', 186: 'fact', 187: 'month', 188: 'different', 189: 'lot', 190: 'study', 191: 'book', 192: 'eye', 193: 'job', 194: 'word', 195: 'though', 196: 'business', 197: 'issue', 198: 'side', 199: 'kind', 200: 'head', 201: 'far', 202: 'black', 203: 'long', 204: 'both', 205: 'little', 206: 'house', 207: 'yes', 208: 'since', 209: 'provide', 210: 'service', 211: 'around', 212: 'friend', 213: 'important', 214: 'father', 215: 'sit', 216: 'away', 217: 'until', 218: 'power', 219: 'hour', 220: 'game', 221: 'often', 222: 'yet', 223: 'line', 224: 'political', 225: 'end', 226: 'among', 227: 'ever', 228: 'stand', 229: 'bad', 230: 'lose', 231: 'however', 232: 'member', 233: 'pay', 234: 'law', 235: 'meet', 236: 'car', 237: 'city', 238: 'almost', 239: 'include', 240: 'continue', 241: 'set', 242: 'later', 243: 'community', 244: 'name', 245: 'once', 246: 'white', 247: 'least', 248: 'president', 249: 'learn', 250: 'real', 251: 'change', 252: 'team', 253: 'minute', 254: 'best', 255: 'several', 256: 'idea', 257: 'lad', 258: 'body', 259: 'information', 260: 'nothing', 261: 'ago', 262: 'lead', 263: 'social', 264: 'understand', 265: 'whether', 266: 'watch', 267: 'together', 268: 'follow', 269: 'parent', 270: 'stop', 271: 'face', 272: 'anything', 273: 'create', 274: 'public', 275: 'already', 276: 'speak', 277: 'others', 278: 'read', 279: 'level', 280: 'allow', 281: 'add', 282: 'office', 283: 'spend', 284: 'door', 285: 'health', 286: 'person', 287: 'art', 288: 'sure', 289: 'war', 290: 'history', 291: 'party', 292: 'within', 293: 'grow', 294: 'result', 295: 'open', 296: 'morning', 297: 'walk', 298: 'reason', 299: 'low', 300: 'win', 301: 'research', 302: 'girl', 303: 'guy', 304: 'early', 305: 'food', 306: 'moment', 307: 'himself', 308: 'air', 309: 'teacher', 310: 'force', 311: 'offer', 312: 'enough', 313: 'education', 314: 'across', 315: 'although', 316: 'remember', 317: 'foot', 318: 'second', 319: 'boy', 320: 'maybe', 321: 'toward', 322: 'able', 323: 'age', 324: 'policy', 325: 'everything', 326: 'love', 327: 'process', 328: 'music', 329: 'including', 330: 'consider', 331: 'appear', 332: 'actually', 333: 'buy', 334: 'probably', 335: 'human', 336: 'wait', 337: 'serve', 338: 'market', 339: 'die', 340: 'send', 341: 'expect', 342: 'sense', 343: 'build', 344: 'stay', 345: 'fall', 346: 'nation', 347: 'plan', 348: 'cut', 349: 'college', 350: 'interest', 351: 'death', 352: 'course', 353: 'someone', 354: 'experience', 355: 'behind', 356: 'reach', 357: 'local', 358: 'kill', 359: 'remain', 360: 'effect', 361: 'yeah', 362: 'suggest', 363: 'class', 364: 'control', 365: 'raise', 366: 'care', 367: 'perhaps', 368: 'late', 369: 'hard', 370: 'field', 371: 'else', 372: 'pass', 373: 'former', 374: 'sell', 375: 'major', 376: 'sometimes', 377: 'require', 378: 'along', 379: 'development', 380: 'themselves', 381: 'report', 382: 'role', 383: 'better', 384: 'economic', 385: 'effort', 386: 'decide', 387: 'rate', 388: 'strong', 389: 'possible', 390: 'heart', 391: 'drug', 392: 'leader', 393: 'light', 394: 'voice', 395: 'wife', 396: 'whole', 397: 'police', 398: 'mind', 399: 'finally', 400: 'pull', 401: 'return', 402: 'free', 403: 'military', 404: 'price', 405: 'less', 406: 'according', 407: 'decision', 408: 'explain', 409: 'son', 410: 'hope', 411: 'develop', 412: 'view', 413: 'relationship', 414: 'carry', 415: 'town', 416: 'road', 417: 'drive', 418: 'arm', 419: 'true', 420: 'federal', 421: 'break', 422: 'difference', 423: 'thank', 424: 'receive', 425: 'value', 426: 'international', 427: 'building', 428: 'action', 429: 'full', 430: 'model', 431: 'join', 432: 'season', 433: 'society', 434: 'tax', 435: 'director', 436: 'position', 437: 'player', 438: 'agree', 439: 'especially', 440: 'record', 441: 'pick', 442: 'wear', 443: 'paper', 444: 'special', 445: 'space', 446: 'ground', 447: 'form', 448: 'support', 449: 'event', 450: 'official', 451: 'whose', 452: 'matter', 453: 'everyone', 454: 'center', 455: 'couple', 456: 'site', 457: 'project', 458: 'hit', 459: 'base', 460: 'activity', 461: 'star', 462: 'table', 463: 'court', 464: 'produce', 465: 'eat', 466: 'teach', 467: 'oil', 468: 'half', 469: 'situation', 470: 'easy', 471: 'cost', 472: 'industry', 473: 'figure', 474: 'street', 475: 'image', 476: 'itself', 477: 'phone', 478: 'either', 479: 'data', 480: 'cover', 481: 'quite', 482: 'picture', 483: 'clear', 484: 'practice', 485: 'piece', 486: 'land', 487: 'recent', 488: 'describe', 489: 'product', 490: 'doctor', 491: 'wall', 492: 'patient', 493: 'worker', 494: 'news', 495: 'test', 496: 'movie', 497: 'certain', 498: 'north', 499: 'personal', 500: 'simply', 501: 'third', 502: 'technology', 503: 'catch', 504: 'step', 505: 'baby', 506: 'computer', 507: 'type', 508: 'attention', 509: 'draw', 510: 'film', 511: 'tree', 512: 'source', 513: 'red', 514: 'nearly', 515: 'organisation', 516: 'choose', 517: 'cause', 518: 'hair', 519: 'century', 520: 'evidence', 521: 'window', 522: 'difficult', 523: 'listen', 524: 'soon', 525: 'culture', 526: 'chance', 527: 'brother', 528: 'energy', 529: 'period', 530: 'summer', 531: 'realise', 532: 'hundred', 533: 'available', 534: 'plant', 535: 'likely', 536: 'opportunity', 537: 'term', 538: 'short', 539: 'letter', 540: 'condition', 541: 'choice', 542: 'single', 543: 'rule', 544: 'daughter', 545: 'administration', 546: 'south', 547: 'husband', 548: 'floor', 549: 'campaign', 550: 'material', 551: 'population', 552: 'economy', 553: 'medical', 554: 'hospital', 555: 'church', 556: 'close', 557: 'thousand', 558: 'risk', 559: 'current', 560: 'fire', 561: 'future', 562: 'wrong', 563: 'involve', 564: 'defence', 565: 'anyone', 566: 'increase', 567: 'security', 568: 'bank', 569: 'myself', 570: 'certainly', 571: 'west', 572: 'sport', 573: 'board', 574: 'seek', 575: 'per', 576: 'subject', 577: 'officer', 578: 'private', 579: 'rest', 580: 'behavior', 581: 'deal', 582: 'performance', 583: 'fight', 584: 'throw', 585: 'top', 586: 'quickly', 587: 'past', 588: 'goal', 589: 'bed', 590: 'order', 591: 'author', 592: 'fill', 593: 'represent', 594: 'focus', 595: 'foreign', 596: 'drop', 597: 'blood', 598: 'upon', 599: 'agency', 600: 'push', 601: 'nature', 602: 'colour', 603: 'recently', 604: 'store', 605: 'reduce', 606: 'sound', 607: 'note', 608: 'fine', 609: 'near', 610: 'movement', 611: 'page', 612: 'enter', 613: 'share', 614: 'common', 615: 'poor', 616: 'natural', 617: 'race', 618: 'concern', 619: 'series', 620: 'significant', 621: 'similar', 622: 'hot', 623: 'language', 624: 'usually', 625: 'response', 626: 'dead', 627: 'rise', 628: 'animal', 629: 'factor', 630: 'decade', 631: 'article', 632: 'shoot', 633: 'east', 634: 'save', 635: 'artist', 636: 'scene', 637: 'stock', 638: 'career', 639: 'despite', 640: 'central', 641: 'thus', 642: 'treatment', 643: 'beyond', 644: 'happy', 645: 'exactly', 646: 'protect', 647: 'approach', 648: 'lie', 649: 'size', 650: 'dog', 651: 'fund', 652: 'serious', 653: 'occur', 654: 'media', 655: 'ready', 656: 'sign', 657: 'thought', 658: 'list', 659: 'individual', 660: 'simple', 661: 'quality', 662: 'pressure', 663: 'accept', 664: 'answer', 665: 'resource', 666: 'identify', 667: 'left', 668: 'meeting', 669: 'determine', 670: 'prepare', 671: 'disease', 672: 'whatever', 673: 'success', 674: 'argue', 675: 'cup', 676: 'particularly', 677: 'amount', 678: 'ability', 679: 'staff', 680: 'recognise', 681: 'indicate', 682: 'character', 683: 'growth', 684: 'loss', 685: 'degree', 686: 'wonder', 687: 'attack', 688: 'herself', 689: 'region', 690: 'box', 691: 'training', 692: 'pretty', 693: 'trade', 694: 'election', 695: 'everybody', 696: 'physical', 697: 'lay', 698: 'general', 699: 'feeling', 700: 'standard', 701: 'bill', 702: 'message', 703: 'fail', 704: 'outside', 705: 'arrive', 706: 'analysis', 707: 'benefit', 708: 'sex', 709: 'forward', 710: 'lawyer', 711: 'present', 712: 'section', 713: 'environmental', 714: 'glass', 715: 'skill', 716: 'sister', 717: 'professor', 718: 'operation', 719: 'financial', 720: 'crime', 721: 'stage', 722: 'compare', 723: 'authority', 724: 'miss', 725: 'design', 726: 'sort', 727: 'act', 728: 'knowledge', 729: 'gun', 730: 'station', 731: 'blue', 732: 'strategy', 733: 'clearly', 734: 'discuss', 735: 'indeed', 736: 'truth', 737: 'song', 738: 'example', 739: 'democratic', 740: 'check', 741: 'environment', 742: 'leg', 743: 'dark', 744: 'various', 745: 'rather', 746: 'laugh', 747: 'guess', 748: 'executive', 749: 'prove', 750: 'hang', 751: 'entire', 752: 'rock', 753: 'forget', 754: 'claim', 755: 'remove', 756: 'manager', 757: 'enjoy', 758: 'network', 759: 'legal', 760: 'religious', 761: 'cold', 762: 'final', 763: 'main', 764: 'science', 765: 'green', 766: 'memory', 767: 'card', 768: 'above', 769: 'seat', 770: 'cell', 771: 'establish', 772: 'nice', 773: 'trial', 774: 'expert', 775: 'spring', 776: 'firm', 777: 'radio', 778: 'visit', 779: 'management', 780: 'avoid', 781: 'imagine', 782: 'tonight', 783: 'huge', 784: 'ball', 785: 'finish', 786: 'yourself', 787: 'theory', 788: 'impact', 789: 'respond', 790: 'statement', 791: 'maintain', 792: 'charge', 793: 'popular', 794: 'traditional', 795: 'onto', 796: 'reveal', 797: 'direction', 798: 'weapon', 799: 'employee', 800: 'cultural', 801: 'contain', 802: 'peace', 803: 'pain', 804: 'apply', 805: 'measure', 806: 'wide', 807: 'shake', 808: 'fly', 809: 'interview', 810: 'manage', 811: 'chair', 812: 'fish', 813: 'particular', 814: 'camera', 815: 'structure', 816: 'politics', 817: 'perform', 818: 'bit', 819: 'weight', 820: 'suddenly', 821: 'discover', 822: 'candidate', 823: 'production', 824: 'treat', 825: 'trip', 826: 'evening', 827: 'affect', 828: 'inside', 829: 'conference', 830: 'unit', 831: 'style', 832: 'adult', 833: 'worry', 834: 'range', 835: 'mention', 836: 'deep', 837: 'edge', 838: 'specific', 839: 'writer', 840: 'trouble', 841: 'necessary', 842: 'throughout', 843: 'challenge', 844: 'fear', 845: 'shoulder', 846: 'institution', 847: 'middle', 848: 'sea', 849: 'dream', 850: 'bar', 851: 'beautiful', 852: 'property', 853: 'instead', 854: 'improve', 855: 'stuff', 856: 'detail', 857: 'method', 858: 'somebody', 859: 'magazine', 860: 'hotel', 861: 'soldier', 862: 'reflect', 863: 'heavy', 864: 'sexual', 865: 'bag', 866: 'heat', 867: 'marriage', 868: 'tough', 869: 'sing', 870: 'surface', 871: 'purpose', 872: 'exist', 873: 'pattern', 874: 'whom', 875: 'skin', 876: 'agent', 877: 'owner', 878: 'machine', 879: 'gas', 880: 'ahead', 881: 'generation', 882: 'commercial', 883: 'address', 884: 'cancer', 885: 'item', 886: 'reality', 887: 'coach', 888: 'yard', 889: 'beat', 890: 'violence', 891: 'total', 892: 'tend', 893: 'investment', 894: 'discussion', 895: 'finger', 896: 'garden', 897: 'notice', 898: 'collection', 899: 'modern', 900: 'task', 901: 'partner', 902: 'positive', 903: 'civil', 904: 'kitchen', 905: 'consumer', 906: 'shot', 907: 'budget', 908: 'wish', 909: 'painting', 910: 'scientist', 911: 'safe', 912: 'agreement', 913: 'capital', 914: 'mouth', 915: 'nor', 916: 'victim', 917: 'threat', 918: 'responsibility', 919: 'smile', 920: 'score', 921: 'account', 922: 'interesting', 923: 'audience', 924: 'rich', 925: 'dinner', 926: 'vote', 927: 'western', 928: 'relate', 929: 'travel', 930: 'debate', 931: 'prevent', 932: 'citizen', 933: 'majority', 934: 'none', 935: 'front', 936: 'born', 937: 'admit', 938: 'senior', 939: 'assume', 940: 'wind', 941: 'key', 942: 'professional', 943: 'mission', 944: 'fast', 945: 'alone', 946: 'customer', 947: 'suffer', 948: 'speech', 949: 'successful', 950: 'option', 951: 'participant', 952: 'southern', 953: 'fresh', 954: 'eventually', 955: 'forest', 956: 'video', 957: 'global', 958: 'reform', 959: 'access', 960: 'restaurant', 961: 'judge', 962: 'publish', 963: 'relation', 964: 'release', 965: 'bird', 966: 'opinion', 967: 'credit', 968: 'critical', 969: 'corner', 970: 'concerned', 971: 'recall', 972: 'version', 973: 'stare', 974: 'safety', 975: 'effective', 976: 'neighbourhood', 977: 'original', 978: 'troop', 979: 'income', 980: 'directly', 981: 'hurt', 982: 'species', 983: 'immediately', 984: 'track', 985: 'basic', 986: 'strike', 987: 'sky', 988: 'freedom', 989: 'absolutely', 990: 'plane', 991: 'nobody', 992: 'achieve', 993: 'object', 994: 'attitude', 995: 'labour', 996: 'refer', 997: 'concept', 998: 'client', 999: 'powerful', 1000: 'perfect', 1001: 'therefore', 1002: 'conduct', 1003: 'announce', 1004: 'conversation', 1005: 'examine', 1006: 'touch', 1007: 'please', 1008: 'attend', 1009: 'completely', 1010: 'variety', 1011: 'sleep', 1012: 'involved', 1013: 'investigation', 1014: 'nuclear', 1015: 'researcher', 1016: 'press', 1017: 'conflict', 1018: 'spirit', 1019: 'replace', 1020: 'encourage', 1021: 'argument', 1022: 'camp', 1023: 'brain' }

#For now..
dic256 = { key:value for key, value in dic1024.items() if key < 256 }
dic256_s = {0: [19, 7, 4], 1: [0, 13, 3], 2: [7, 0, 21, 4], 3: [19, 7, 0, 19], 4: [5, 14, 17], 5: [24, 14, 20], 6: [22, 8, 19, 7], 7: [18, 0, 24], 8: [19, 7, 8, 18], 9: [19, 7, 4, 24], 10: [1, 20, 19], 11: [7, 8, 18], 12: [5, 17, 14, 12], 13: [13, 14, 19], 14: [18, 7, 4], 15: [22, 7, 0, 19], 16: [19, 7, 4, 8, 17, 29], 17: [2, 0, 13], 18: [22, 7, 14], 19: [6, 4, 19], 20: [22, 14, 20, 11, 3, 29], 21: [7, 4, 17], 22: [0, 11, 11], 23: [12, 0, 10, 4], 24: [0, 1, 14, 20, 19, 29], 25: [10, 13, 14, 22], 26: [22, 8, 11, 11], 27: [14, 13, 4], 28: [19, 8, 12, 4], 29: [19, 7, 4, 17, 4, 29], 30: [24, 4, 0, 17], 31: [19, 7, 8, 13, 10, 29], 32: [22, 7, 4, 13], 33: [22, 7, 8, 2, 7, 29], 34: [19, 7, 4, 12], 35: [18, 14, 12, 4], 36: [15, 4, 14, 15, 11, 4], 37: [19, 0, 10, 4], 38: [14, 20, 19], 39: [8, 13, 19, 14], 40: [9, 20, 18, 19], 41: [18, 4, 4], 42: [7, 8, 12], 43: [24, 14, 20, 17], 44: [2, 14, 12, 4], 45: [2, 14, 20, 11, 3, 29], 46: [13, 14, 22], 47: [19, 7, 0, 13], 48: [11, 8, 10, 4], 49: [14, 19, 7, 4, 17, 29], 50: [7, 14, 22], 51: [19, 7, 4, 13], 52: [8, 19, 18], 53: [14, 20, 17], 54: [12, 14, 17, 4], 55: [19, 7, 4, 18, 4, 29], 56: [22, 0, 13, 19], 57: [22, 0, 24], 58: [11, 14, 14, 10], 59: [5, 8, 17, 18, 19, 29], 60: [0, 11, 18, 14], 61: [13, 4, 22], 62: [1, 4, 2, 0, 20, 18, 4, 29], 63: [3, 0, 24], 64: [20, 18, 4], 65: [12, 0, 13], 66: [5, 8, 13, 3], 67: [7, 4, 17, 4], 68: [19, 7, 8, 13, 6, 29], 69: [6, 8, 21, 4], 70: [12, 0, 13, 24], 71: [22, 4, 11, 11], 72: [14, 13, 11, 24], 73: [19, 7, 14, 18, 4, 29], 74: [19, 4, 11, 11], 75: [21, 4, 17, 24], 76: [4, 21, 4, 13], 77: [1, 0, 2, 10], 78: [0, 13, 24], 79: [6, 14, 14, 3], 80: [22, 14, 12, 0, 13, 29], 81: [19, 7, 17, 14, 20, 6, 7, 29], 82: [11, 8, 5, 4], 83: [2, 7, 8, 11, 3, 29], 84: [22, 14, 17, 10], 85: [3, 14, 22, 13], 86: [12, 0, 24], 87: [0, 5, 19, 4, 17, 29], 88: [18, 7, 14, 20, 11, 3], 89: [2, 0, 11, 11], 90: [22, 14, 17, 11, 3, 29], 91: [14, 21, 4, 17], 92: [18, 2, 7, 14, 14, 11], 93: [18, 19, 8, 11, 11, 29], 94: [19, 17, 24], 95: [11, 0, 18, 19], 96: [0, 18, 10], 97: [13, 4, 4, 3], 98: [19, 14, 14], 99: [5, 4, 4, 11], 100: [18, 19, 0, 19, 4, 29], 101: [13, 4, 21, 4, 17, 29], 102: [1, 4, 2, 14, 12, 4], 103: [1, 4, 19, 22, 4, 4, 13, 29], 104: [7, 8, 6, 7], 105: [17, 4, 0, 11, 11, 24], 106: [18, 14, 12, 4, 19, 7, 8, 13, 6], 107: [12, 14, 18, 19], 108: [0, 13, 14, 19, 7, 4, 17, 29], 109: [12, 20, 2, 7], 110: [5, 0, 12, 8, 11, 24], 111: [14, 22, 13], 112: [11, 4, 0, 21, 4, 29], 113: [15, 20, 19], 114: [14, 11, 3], 115: [22, 7, 8, 11, 4, 29], 116: [12, 4, 0, 13], 117: [10, 4, 4, 15], 118: [18, 19, 20, 3, 4, 13, 19, 29], 119: [22, 7, 24], 120: [11, 4, 19], 121: [6, 17, 4, 0, 19, 29], 122: [18, 0, 12, 4], 123: [1, 8, 6], 124: [6, 17, 14, 20, 15, 29], 125: [1, 4, 6, 8, 13, 29], 126: [18, 4, 4, 12], 127: [2, 14, 20, 13, 19, 17, 24, 29], 128: [7, 4, 11, 15], 129: [19, 0, 11, 10], 130: [22, 7, 4, 17, 4, 29], 131: [19, 20, 17, 13], 132: [15, 17, 14, 1, 11, 4, 12, 29], 133: [4, 21, 4, 17, 24, 29], 134: [18, 19, 0, 17, 19, 29], 135: [7, 0, 13, 3], 136: [12, 8, 6, 7, 19, 29], 137: [18, 7, 14, 22], 138: [15, 0, 17, 19], 139: [0, 6, 0, 8, 13, 18, 19, 29], 140: [15, 11, 0, 2, 4, 29], 141: [18, 20, 2, 7], 142: [0, 6, 0, 8, 13, 29], 143: [5, 4, 22], 144: [2, 0, 18, 4], 145: [22, 4, 4, 10], 146: [2, 14, 12, 15, 0, 13, 24, 29], 147: [18, 24, 18, 19, 4, 12], 148: [4, 0, 2, 7], 149: [17, 8, 6, 7, 19, 29], 150: [15, 17, 14, 6, 17, 0, 12, 29], 151: [7, 4, 0, 17], 152: [16, 20, 4, 18, 19, 8, 14, 13], 153: [3, 20, 17, 8, 13, 6], 154: [15, 11, 0, 24], 155: [6, 14, 21, 4, 17, 13, 12, 4, 13, 19, 29], 156: [17, 20, 13], 157: [18, 12, 0, 11, 11, 29], 158: [13, 20, 12, 1, 4, 17], 159: [14, 5, 5], 160: [0, 11, 22, 0, 24, 18], 161: [12, 14, 21, 4], 162: [13, 8, 6, 7, 19, 29], 163: [11, 8, 21, 4], 164: [15, 14, 8, 13, 19, 29], 165: [1, 4, 11, 8, 4, 21, 4, 29], 166: [7, 14, 11, 3], 167: [19, 14, 3, 0, 24, 29], 168: [1, 17, 8, 13, 6, 29], 169: [7, 0, 15, 15, 4, 13], 170: [13, 4, 23, 19], 171: [22, 8, 19, 7, 14, 20, 19, 29], 172: [1, 4, 5, 14, 17, 4], 173: [11, 0, 17, 6, 4, 29], 174: [12, 20, 18, 19], 175: [7, 14, 12, 4], 176: [20, 13, 3, 4, 17, 29], 177: [22, 0, 19, 4, 17, 29], 178: [17, 14, 14, 12], 179: [22, 17, 8, 19, 4, 29], 180: [12, 14, 19, 7, 4, 17], 181: [0, 17, 4, 0], 182: [13, 0, 19, 8, 14, 13, 0, 11], 183: [12, 14, 13, 4, 24, 29], 184: [18, 19, 14, 17, 24, 29], 185: [24, 14, 20, 13, 6, 29], 186: [5, 0, 2, 19], 187: [12, 14, 13, 19, 7, 29], 188: [3, 8, 5, 5, 4, 17, 4, 13, 19], 189: [11, 14, 19], 190: [18, 19, 20, 3, 24, 29], 191: [1, 14, 14, 10], 192: [4, 24, 4], 193: [9, 14, 1], 194: [22, 14, 17, 3], 195: [19, 7, 14, 20, 6, 7], 196: [1, 20, 18, 8, 13, 4, 18, 18], 197: [8, 18, 18, 20, 4, 29], 198: [18, 8, 3, 4], 199: [10, 8, 13, 3], 200: [7, 4, 0, 3], 201: [5, 0, 17], 202: [1, 11, 0, 2, 10, 29], 203: [11, 14, 13, 6], 204: [1, 14, 19, 7], 205: [11, 8, 19, 19, 11, 4], 206: [7, 14, 20, 18, 4, 29], 207: [24, 4, 18], 208: [18, 8, 13, 2, 4, 29], 209: [15, 17, 14, 21, 8, 3, 4, 29], 210: [18, 4, 17, 21, 8, 2, 4, 29], 211: [0, 17, 14, 20, 13, 3], 212: [5, 17, 8, 4, 13, 3], 213: [8, 12, 15, 14, 17, 19, 0, 13, 19], 214: [5, 0, 19, 7, 4, 17], 215: [18, 8, 19], 216: [0, 22, 0, 24], 217: [20, 13, 19, 8, 11, 29], 218: [15, 14, 22, 4, 17, 29], 219: [7, 14, 20, 17], 220: [6, 0, 12, 4], 221: [14, 5, 19, 4, 13, 29], 222: [24, 4, 19], 223: [11, 8, 13, 4], 224: [15, 14, 11, 8, 19, 8, 2, 0, 11], 225: [4, 13, 3], 226: [0, 12, 14, 13, 6, 29], 227: [4, 21, 4, 17], 228: [18, 19, 0, 13, 3, 29], 229: [1, 0, 3], 230: [11, 14, 18, 4], 231: [7, 14, 22, 4, 21, 4, 17, 29], 232: [12, 4, 12, 1, 4, 17], 233: [15, 0, 24], 234: [11, 0, 22], 235: [12, 4, 4, 19], 236: [2, 0, 17], 237: [2, 8, 19, 24], 238: [0, 11, 12, 14, 18, 19], 239: [8, 13, 2, 11, 20, 3, 4, 29], 240: [2, 14, 13, 19, 8, 13, 20, 4], 241: [18, 4, 19], 242: [11, 0, 19, 4, 17, 29], 243: [2, 14, 12, 12, 20, 13, 8, 19, 24], 244: [13, 0, 12, 4], 245: [14, 13, 2, 4], 246: [22, 7, 8, 19, 4, 29], 247: [11, 4, 0, 18, 19, 29], 248: [15, 17, 4, 18, 8, 3, 4, 13, 19], 249: [11, 4, 0, 17, 13, 29], 250: [17, 4, 0, 11], 251: [2, 7, 0, 13, 6, 4], 252: [19, 4, 0, 12], 253: [12, 8, 13, 20, 19, 4], 254: [1, 4, 18, 19], 255: [18, 4, 21, 4, 17, 0, 11, 29]}

dict_reverse = []
for w in dic1024:
	dict_reverse.append(dic1024[w])

def load_dict(filename):
    dic1024 = {}
    f = open(filename,'r')
    for i in range(0,1024):
        cw = f.readline()
        if(len(cw.rstrip()) > 2): dic1024[i] = cw.rstrip()
	
    dict_reverse = []
    for w in dic1024:
        dict_reverse.append(dic1024[w])		     
   
def search_dict(word):
	if(word in dict_reverse):
		return dict_reverse.index(word)
	else: return -1

def shift(val,amt):
    if(amt >= 0):
        return(val << amt)
    elif(amt < 0):
        return(val >> abs(amt))

class Substitute:
    
    def __init__(self):
        self.dict_last = False
        self.dict_fchar = 0
        self.unicode_len = 0
        self.unicode_buffer = []

    #Desub functions
    def __desub_lcase(self,a):
        #Character greater than 26 = Mode switch      
        return(std_chars_decode[a])
                   
    def __desub_ucase(self,a):
        return((0,chr(a + 65)))
        
    def __desub_num(self,a):
        return((0,chr(a + 33)))

    def __desub_dic1024(self,a):
        if(not self.dict_last):
            self.dict_fchar = a
            self.dict_last = True
            return((4,""))
        else:
            self.dict_last = False
            return(0,dic1024[((self.dict_fchar << 5) | a)] + " ")
        
    def __desub_unicode(self,a):
        if(self.unicode_len == 0):
            self.unicode_len = a
            return((5,""))
        elif(self.unicode_len > 0):
            self.unicode_buffer.append(a)
            
            if(self.unicode_len == len(self.unicode_buffer)):
                char = self.__get_unicode(self.unicode_buffer)
                self.unicode_len = 0
                self.unicode_buffer = []
                return((0,char))
            return((5,""))
        
    #Unicode gen/get
    def __gen_unicode(self,char):
        ordn = ord(char)
        bl = ordn.bit_length()
        li = [31,ceil((bl) / 5)]

        for i in range(0,li[1]):
            li.append(((ordn >> 5*i) & 31))

        return li

    def __get_unicode(self,clist):
        ccode = 0
        for i in range(0,len(clist)):
            ccode = (ccode << 5) + (clist[len(clist) - i - 1] & 31)
        return chr(ccode)

    def desub(self,charlist,usedict = True):
        self.unicode_len = 0 # Reset unicode len
        self.unicode_buffer = [] # and buffer
        
        mos = {0:self.__desub_lcase,1:self.__desub_ucase,2:self.__desub_num,4:self.__desub_dic1024,5:self.__desub_unicode}
        cl = []
        mode = 0

        for a in charlist:
            (mode,st) = mos[mode](a)
            cl.append(st)

        #Cut off trailing space if last mode was a dictionary word
        if len(cl[-1]) > 2: cl[-1] = cl[-1].strip()
        if (len(cl[-2]) > 2) and (charlist[-1] == 29): cl[-2] = cl[-2].strip()    
        return "".join(cl)
        
    def dictsub(self,cl):
        return cl    

    def sub(self,str_in,usedict = True):
        #dict_check = True #Do not check dictionary if a unicode/uppercase/num character has been used in current word
        word = []
        cl = []
        for a in str_in:   
            if(usedict): word.append(a)
            c_num = ord(a)         
            if(c_num in range(97,123)): cl.append(c_num - 97)
		
	
            elif(c_num in range(65,97)): #Upper case and [\]^_`
                dict_check = False
                cl.extend([27,c_num - 65])

            elif(c_num == 32): #Space
                cl.append(26)

             #   if(usedict and dict_check): # Check if word exists in dictionary
             #       wrdtxt = "".join(word)[:-1]            
             #       if(wrdtxt in dict_reverse):
             #            wordcode = dict_reverse.index(wrdtxt) 
             #            cl = cl[:len(cl) - (len(word))]
             #            cl.extend([30,wordcode >> 5,wordcode & 31])
             #       word = []
             #   dict_check = True

            elif(c_num in range(33,65)): 
                cl.extend(num_chars[c_num])
                #dict_check = False
            #elif(c_num in range(32,65)): cl.extend(num_chars[c_num])            
                
            else:
                #dict_check = False
                #UTF-8
                cl.extend(self.__gen_unicode(a))

        #Check if last word is a dictionary word
        #if(usedict): # Check if word exists in dictionary
        #        wordcode = search_dict("".join(word))    
        #        if(wordcode != -1):
        #                cl = cl[:len(cl) - (len(word))]
        #                cl.extend([30,wordcode >> 5,wordcode & 31])

        #Check if str_in ends with a space, and last value added was a dictionary word
        #if( (str_in[-1] == " ") and (cl[-3] == 30)): cl.append(27)

        #Throw in blank character if more than 5 bits free
        BitsFree = 8 - (len(cl) * 5) % 8
        if( (BitsFree > 4) and (BitsFree != 8) ):
            cl.append(29)
            

        if(usedict == False): return cl
        else: return self.dictsub(cl)
        

        


def encode(charlist):
    #Converts a list of 5-bit values (0-31) into byte string
    nexstep = {0:(5,3), 1:(6,2), 2:(7,1), 3:(0,0), 4:(1,-1,1,7), 5:(2,-2,3,6), 6:(3,-3,7,5), 7:(4,-4,15,4) }
    curbyte = 0
    bstr = []
    lastbit = []
    step = 0
        
    ByteLeft = False
    
    bistro = []

    #as_num = (a[0] << 35) + (a[1] << 30) + (a[2] << 25) + (a[3] << 20) + (a[4] << 15) + (a[5] << 10) + (a[6] << 5) + a[7] 
    #For speed we encode 8 characters at a time (40b)
    for f in range(int(len(charlist) / 8)):
        thisbit = charlist[f*8:(f*8)+8]
        as_num = (thisbit[0] << 35) + (thisbit[1] << 30) + (thisbit[2] << 25) + (thisbit[3] << 20) + (thisbit[4] << 15) + (thisbit[5] << 10) + (thisbit[6] << 5) + thisbit[7]
        bistro.append(as_num.to_bytes(5,'big'))             


    if(len(charlist) % 8 > 0): #Catch remaining characters
        lastbit = charlist[0-(len(charlist)%8):]

    for a in lastbit:
        curbyte = curbyte | shift(a,nexstep[step][1])
        ByteLeft = True
        if(step > 2):
            bstr.append(curbyte)
            curbyte = 0
            ByteLeft = False
            if(step > 3):
                curbyte = (a & nexstep[step][2]) << nexstep[step][3]
                ByteLeft = True
        step = nexstep[step][0]
        
    if ByteLeft:
        bstr.append(curbyte)
    
    #return bytes(bstr)
    return b''.join(bistro) + bytes(bstr)

def drawchars(byte,nbits,nbitsl):
    tot = 8 + nbitsl
    itot = (nbits << 8) | byte
    if(tot < 10):
        c1 = itot >> (tot - 5) & 31
        newnbits = itot & (2**(tot -5) -1)
        newnbitsl = tot - 5
        return(([c1],newnbits,newnbitsl))
    elif(tot > 9):
         c1 = itot >> (tot - 5) & 31
         c2 = itot >> (tot - 10) & 31
         newnbits = itot & (2**(tot - 10)-1)
         newnbitsl = tot - 10
         return(([c1,c2],newnbits,newnbitsl))
    
def decode(string):
    bs = bytes(string)
    nbl = 0
    nbs = 0
    ls = []
    ns = None
    as_num = 0
    lastbit = b''
    #Try to get 5 bytes at a time first for a while
    for b in range(int(len(bs)/5)):
        as_num = as_num.from_bytes(bs[b*5:(b*5)+5],'big')                
        ls.extend([as_num >> 35, (as_num >> 30) & 31, (as_num >> 25) & 31, (as_num >> 20) & 31, (as_num >> 15) & 31, (as_num >> 10) & 31, (as_num >> 5) & 31, as_num & 31])

    if(len(bs) % 5 > 0): #Catch remaining characters
        lastbit = bs[0-(len(bs)%5):]

        for a in lastbit:
            rs = drawchars(a,nbs,nbl)
            nbs = rs[1]
            nbl = rs[2]
            ls.extend(rs[0])
    return ls

s = Substitute()

dic256_s = {}

for a in dic256:
    dic256_s[a] = s.sub(dic256[a])

print(dic256_s)

def compress(string,usedict = True):
    return(encode(s.sub(string,usedict)))

def decompress(string):
   return(s.desub(decode(string)))