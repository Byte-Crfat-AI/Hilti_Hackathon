import torch  # Import torch at the beginning
from main_keyword_extraction import MainKeywordExtraction
from embeddings import Embeddings
from keyword_ranking import Keyword
from vectordb import VectorDB

def embeddings():
    print("=== Generating Text Embeddings ===")
    text = "Natural Language Processing (NLP) involves the application of computational techniques to the analysis and synthesis of natural language."
    embeddings_class = Embeddings()
    embeddings = embeddings_class.get_embeddings(text)
    print("Embeddings generated (shape):", embeddings.shape)

def keyword_ranking():
    print("\n=== Extracting and Ranking Keywords ===")
    text = "Machine learning is a subset of artificial intelligence that involves training algorithms to learn from and make predictions on data."
    keyword_class = Keyword()
    ranked_set = keyword_class.keyword_main(text)
    print("Ranked Keywords and Scores:")
    for embedding, rank, keyword in ranked_set:
        print(f"Keyword: {keyword}, Score: {rank}")

def vectordb():
    print("\n=== Storing Keywords in VectorDB ===")
    ranked_set = [
        [torch.tensor([1.0, 2.0, 3.0]), 0.9, "machine learning"],
        [torch.tensor([4.0, 5.0, 6.0]), 0.8, "artificial intelligence"],
    ]
    path = "D:/Hilti_Hackathon/Example/path/to/file.txt"
    vector_db = VectorDB()
    vector_db.keywords_db(ranked_set, path)
    print("Keywords stored in VectorDB.")

def main_keyword_extraction():
    print("\n=== Full Pipeline for Keyword Extraction ===")
    processed_files = [
        (
            '''I DON'T ACTIVELY want to die. Not all the time.

            If it weren't for my father, then sure I'd consider it. He may not be my favorite person in the world, and I am definitely not his, but I don't relish the thought of him standing at my gravesite, hunched over my coffin, racked with sobs. I only think about dying sometimes-like now.

            We're almost at Hades Point. In approximately two minutes and thirty seconds, the black Lorax I'm riding in will carry me past the infamous cliff's edge, where, historically twelve students at my school have plummeted to their deaths. I'm not afraid of the point, but maybe I should be. It's deep-Grand Canyon deep. A gaping mouth in the ground that swallows kids who can't handle Darkwood Academy. That's the boarding school I go to in Vermont, where I'm starting my junior year. It's where I spent my first year and sophomore year, too, before the thing that happened. But more on that...never.

            "Approaching Hades Point!" trills a merry voice, invading my thoughts. You'd think a driverless vehicle would guarantee a person some peace and quiet, but no. When the Lorax picked me up at the Burlington airport two hours ago, the operating system forced me to select a name for its virtual driver. I'd rejected the suggested monikers and typed in one of my own choosing: Misery.

            "This is Misery, your friendly chauffeur!" the voice had immediately chirped at me. She hadn't stopped to take a metaphorical breath since.

            Misery continues her assault on my ears. "If you look to your left, Miss. Chance, you'll see we're passing Hades Point, one of the most scenic spots on campus!"

            Sure, Misery. I take in the precipitous drop as we round the bend. If by "scenic" you mean deadly.

            I stare at Hades Point laid out in the distance like a casket. I picture them, all twelve students who tumbled over.''',
            "D:/Hilti_Hackathon/Example/path1/to/file1.txt",
        ),
        (
            '''Sounds of laughter. Sounds of screaming. Sparkles from a wood fire out of sight. It was dark. I sat up, bewildered. This wasn’t my bedroom. A horse neighed. A horse?

            I looked down at two small wrists and hands, bound by heavy rope. Delicate, feminine hands, long nails. Except for the fourth finger on the left hand, nail’s broken there. I was wearing a deep blue, heavy dress. It had to be a dream. It didn’t feel like a dream. But this wasn’t my body! I’m a guy, I don’t wear dresses. Or indulge in bondage fantasies. Often.

            Campfire smoke drifted over, sparks flew up into the night. Some distance away, a silhouette by the fire rose, arched his head back as he finished off a mug. He set that down, laughed, and his shadow shifted toward me and slowly got bigger. Outlined by the flames, I couldn’t see his features, but his gait was heavy, with a lumbering, side to side motion.

            Pushing my bound feet against the ground, I slid backward until I hit a large tree.

            “That’s right, missy, nowhere to run.” He barked out a laugh. “Let’s see what royalty looks like up close!” Dirt caked his face and hands, his clothing was heavy and worn. Fading browns on weathered leather. Like someone out of a postapocalyptic movie. A black eye and a long bruise under it.

            I couldn’t crawl away, not bound like this. To my right, some distance away, more figures tied to stakes, twitching and moaning. A dozen feet to my left a lone prisoner locked in thick handcuffs, a rope tightly around his mouth as a gag, cutting into his cheeks. He gave me a sad look and shook his head, as if apologizing.

            Yeah. I was ready for this dream to end. Going to have to hit up a therapist after this one.

            But it didn’t end, and he knelt down in front of me. Acrid smells of sweat, blood and piss assaulted my nose. He pulled out a long, thin dagger.

            “What’s amatter, Princess? You don’ like me?” He grabbed the rope around my ankles, sliding me down the tree trunk until I was on my back, then sliced through it, freeing my legs. “You’ll spread ‘em all the same.” He sheathed the long knife, started undoing the rope around his pants.

            Ok, ok, ok, I thought, my heart pounding, this wasn’t happening. Not a chance! For one thing, I wasn’t a damned princess! I reached around on the ground with my bound hands, looking for something, anything. Having found it, I sat up.

            “Want a closer look, eh?” Standing in front of me, his pants falling down, the stench worsened and he flashed me a broken toothed smile. I smiled back and with both hands smashed a heavy stone into his balls as hard as I could.

            “Aaah!” he screamed, doubling over.

            I slammed the stone into his temple. He fell sideways, landing hard, body twitching slightly. I stared in disbelief for too many moments, dropped the rock, grabbed his long knife, planted the tip into the ground and ran the ropes around my wrists along the blade until they came apart.

            The other man was straining to get my attention. Hell, I figured if he was tied up, he was on my side. I cut through his gag, then the rope tying him to the ground. The knife couldn’t do anything against the metal around his wrists, though.

            “Princess! I let you down, I’m so sorry.”

            “Never mind that. What the hell is going on?”

            He stared at me in disbelief. “We . . . we need to get out of here. Quickly! If that’s possible.”''',
            "D:/Hilti_Hackathon/Example/path2/to/file2.txt",
        ),
    ]
    main_extraction = MainKeywordExtraction()
    result = main_extraction.main_keyword_extraction(processed_files)  # Use the correct method name
    print(result)

if __name__ == "__main__":
    main_keyword_extraction()
