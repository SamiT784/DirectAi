"""
DIRECTORAI PROMPTS GUIDE
How to create effective prompts for historical shorts
"""

# ============================================================================
# WHAT ARE PROMPTS?
# ============================================================================

Prompts are historical ideas/stories that DirectorAI will convert into
cinematic YouTube Shorts. Think of them as short summaries of historical
events or figures that you want to see visualized.

Format: JSON file with array of strings
Location: /content/DirectorAI/prompts.json (in Colab)


# ============================================================================
# PROMPT FILE FORMAT
# ============================================================================

{
  "ideas": [
    "Historical idea 1",
    "Historical idea 2",
    "Historical idea 3"
  ]
}

Example:

{
  "ideas": [
    "Cleopatra VII ruling ancient Egypt",
    "The eruption of Mount Vesuvius in 79 AD",
    "Joan of Arc leading the French army"
  ]
}


# ============================================================================
# WHAT MAKES A GOOD PROMPT?
# ============================================================================

✓ GOOD PROMPTS HAVE:

1. SPECIFIC PERSON OR GROUP
   - "Cleopatra VII"
   - "300 Spartans at Thermopylae"
   - "Joan of Arc"
   - "Genghis Khan"

2. SPECIFIC EVENT
   - "The rise to power"
   - "A great battle"
   - "The eruption"
   - "The conquest"
   - "The betrayal"

3. TIME PERIOD
   - "Ancient Egypt"
   - "Medieval Europe"
   - "During the Hundred Years' War"
   - "79 AD"
   - "15th century"

4. EMOTIONAL/DRAMATIC CONTEXT
   - "Against overwhelming odds"
   - "Despite political opposition"
   - "Driven by divine faith"
   - "Seeking revenge"
   - "Fighting for freedom"

5. LENGTH: 1-3 SENTENCES
   - Not too short (no detail)
   - Not too long (hard to process)

TOTAL LENGTH: 100-300 characters per idea


# ============================================================================
# EXAMPLES OF GOOD PROMPTS
# ============================================================================

EXAMPLE 1: Historical Figure
"Cleopatra VII, the last pharaoh of ancient Egypt, navigating complex political 
intrigue and diplomacy to maintain her kingdom's independence against the 
expanding Roman Empire"

EXAMPLE 2: Military Event
"The Battle of Thermopylae in 480 BC, where 300 elite Spartan warriors made their 
legendary last stand against a massive Persian army, sacrificing themselves to 
defend Greek freedom"

EXAMPLE 3: Natural Disaster
"The eruption of Mount Vesuvius in 79 AD, a catastrophic volcanic event that buried 
the Roman cities of Pompeii and Herculaneum, forever preserving their citizens in 
volcanic ash"

EXAMPLE 4: Religious Figure
"Joan of Arc, a peasant girl in medieval France, leading armies during the Hundred 
Years' War, driven by her unwavering faith in divine destiny to save her nation"

EXAMPLE 5: Conquest
"Hannibal Barca, the brilliant Carthaginian general, making the daring strategic 
decision to cross the Alps with war elephants to attack Rome during the Second 
Punic War"

EXAMPLE 6: Exploration
"The Viking settlement of Vinland, Norse explorers crossing the Atlantic Ocean 
centuries before Columbus, establishing the first known European settlement in 
North America"

EXAMPLE 7: Fall of Empire
"The fall of Constantinople in 1453, the final moment of the Byzantine Empire as 
Ottoman forces breached the ancient city's legendary walls after over 1000 years 
of continuous rule"

EXAMPLE 8: Cultural Landmark
"The Library of Alexandria burning down, humanity's greatest repository of ancient 
knowledge consumed by flames, taking centuries of accumulated wisdom and scientific 
advancement with it"


# ============================================================================
# EXAMPLES OF BAD PROMPTS
# ============================================================================

✗ TOO VAGUE:
- "Ancient history"
- "A war"
- "Stuff about emperors"
- "Something historical"

✗ TOO GENERIC:
- "Kings fighting"
- "People in the past"
- "Old times"

✗ TOO LONG:
- "A very detailed description spanning multiple sentences with lots of information about 
   the specific historical figure and all the complicated political circumstances that led 
   to the event in question during this particular time period..."

✗ MISSING CONTEXT:
- "The battle" (which battle? when? who?)
- "He was born" (who is he?)
- "A volcano erupted" (when? where? why important?)


# ============================================================================
# CREATING YOUR PROMPTS FILE
# ============================================================================

OPTION 1: Use Sample File (EASIEST)
1. Copy sample_prompts.json
2. Modify the ideas to your preference
3. Save as prompts.json

OPTION 2: Create New File
1. Create text file with JSON structure
2. Add your historical ideas
3. Save as prompts.json

OPTION 3: In Google Colab
Copy this Colab cell and customize:

prompts = {
    "ideas": [
        "Your first historical idea here",
        "Your second historical idea here",
        "Your third historical idea here"
    ]
}

import json
with open('/content/DirectorAI/prompts.json', 'w') as f:
    json.dump(prompts, f, indent=2)


# ============================================================================
# PROMPT IDEAS BY CATEGORY
# ============================================================================

ANCIENT HISTORY:
- "Cleopatra VII navigating politics in ancient Egypt"
- "Julius Caesar crossing the Rubicon"
- "The eruption of Mount Vesuvius destroying Pompeii"
- "Tutankhamun ruling as a young pharaoh"
- "Augustus becoming the first Roman Emperor"

MEDIEVAL PERIOD:
- "Joan of Arc leading French armies to victory"
- "King Richard the Lionheart in the Crusades"
- "The Norman Conquest of England in 1066"
- "Charlemagne building his vast empire"
- "The Byzantine Empire's thousand-year rule"

MILITARY HISTORY:
- "The Battle of Thermopylae with 300 Spartans"
- "Hannibal crossing the Alps with war elephants"
- "The Viking raids on European settlements"
- "Napoleon's rise and fall"
- "The Mongol Empire under Genghis Khan"

EXPLORATION:
- "Columbus discovering the New World"
- "Magellan's circumnavigation of the Earth"
- "The Viking settlement of Vinland"
- "Marco Polo traveling the Silk Road"
- "Zheng He's voyages across the Indian Ocean"

WOMEN IN HISTORY:
- "Nefertiti as queen of ancient Egypt"
- "Eleanor of Aquitaine shaping medieval politics"
- "Queen Elizabeth I leading England through crisis"
- "Hatshepsut as female pharaoh of Egypt"
- "Catherine the Great expanding the Russian Empire"

EMPIRE & CONQUEST:
- "The fall of Constantinople in 1453"
- "The rise of the Ottoman Empire"
- "The Mongol conquest across Asia"
- "Alexander the Great's eastern campaigns"
- "The spread of the Roman Empire"


# ============================================================================
# TIPS FOR MAXIMUM IMPACT
# ============================================================================

1. MIX TIME PERIODS
   Don't just do ancient Egypt - vary the eras
   This creates diversity in your shorts

2. INCLUDE DRAMA
   Words that evoke emotion:
   - Rise / Fall
   - Victory / Defeat
   - Betrayal / Loyalty
   - Against odds / Overwhelming force
   - Divine / Legendary / Legendary

3. BE SPECIFIC ABOUT TIME
   "15th century Europe" not just "medieval times"
   "79 AD" not just "ancient times"

4. MENTION FAMOUS NAMES
   People recognize:
   - Cleopatra
   - Julius Caesar
   - Joan of Arc
   - Genghis Khan
   - Napoleon

5. INCLUDE ACTION VERBS
   - Leading armies
   - Conquering empires
   - Defending kingdoms
   - Discovering continents
   - Betraying allies

6. START WITH HOOK
   Begin each idea with something interesting
   "The rise of..." (not just "Biography of...")
   "The legendary..." (not just "The...")


# ============================================================================
# HOW DIRECTORAI USES YOUR PROMPTS
# ============================================================================

For each prompt, DirectorAI will:

1. SCRIPT ENGINE
   Read your prompt → Generate detailed cinematic script

2. PROMPT ENGINE
   Script → Generate visual prompts for each scene

3. NARRATION ENGINE
   Script → Generate voice narration

4. SCENE ENGINE
   Visual prompts → Generate and animate images

5. INTERPOLATION ENGINE
   Animation → Smooth the motion

6. RENDER ENGINE
   All together → Final YouTube Short


# ============================================================================
# MONITORING YOUR PROMPTS
# ============================================================================

In Google Colab, check progress:

import json
from pathlib import Path

queue_file = Path('/content/DirectorAI/queue.json')
with open(queue_file, 'r') as f:
    queue_data = json.load(f)

for job in queue_data['jobs']:
    print(f"ID {job['job_id']}: {job['status']} - {job['idea']}")


# ============================================================================
# TROUBLESHOOTING PROMPTS
# ============================================================================

PROBLEM: "Invalid JSON"
FIX: Use online JSON validator: https://jsonlint.com/

PROBLEM: "No ideas found"
FIX: Check structure:
  { "ideas": [ ... ] }  ← Correct
  { "prompts": [ ... ] } ← Wrong key name

PROBLEM: "Ideas too vague, low quality outputs"
FIX: Add more specifics to prompts
  Before: "A battle"
  After: "The Battle of Thermopylae with 300 Spartans against Persia"

PROBLEM: "Too many ideas, generation takes too long"
FIX: Start with 5-10, increase gradually
  Keep total generation time under 5 hours per session


# ============================================================================
# BEST PRACTICES SUMMARY
# ============================================================================

DO:
✓ Use specific names and dates
✓ Include emotion and drama
✓ Write 1-3 sentences per idea
✓ Test with 3-5 ideas first
✓ Verify JSON syntax
✓ Mix different time periods
✓ Focus on famous historical events

DON'T:
✗ Write vague descriptions
✗ Use only names without context
✗ Write paragraphs (too long)
✗ Mix fantasy with history
✗ Use modern references
✗ Leave prompts empty
✗ Use non-ASCII characters


# ============================================================================
# EXAMPLES FOR YOUR FIRST RUN
# ============================================================================

Copy this to prompts.json to start:

{
  "ideas": [
    "Cleopatra VII, the last pharaoh of ancient Egypt, navigating diplomatic crises and maintaining her independence against Rome",
    "The eruption of Mount Vesuvius in 79 AD, instantly burying Pompeii and freezing its citizens forever",
    "Joan of Arc leading French armies to victory during the Hundred Years' War, driven by her unshakeable faith"
  ]
}

Then customize with your own ideas!


# ============================================================================
# READY?
# ============================================================================

1. Create your prompts.json
2. Validate JSON syntax
3. Upload to Colab
4. Run generation
5. Download results

Good luck! 🎬📹
