// Curated dataset of famous Maharashtra forts
// Each fort has rich metadata for filtering, recommendations, and AI Q&A

export const FORTS = [
  {
    id: 'rajgad', name: 'Rajgad Fort', district: 'Pune', type: 'Hill Fort',
    difficulty: 'Hard', elevation: 1376, season: 'Monsoon, Winter',
    water: 'Year-round', accommodation: 'Caves',
    coordinates: { lat: 18.2466, lng: 73.6810 },
    image: 'https://images.pexels.com/photos/14229957/pexels-photo-14229957.jpeg',
    summary: 'The first capital of the Maratha Empire under Chhatrapati Shivaji Maharaj, perched at 1376m on the Sahyadris.',
    history: 'Originally known as Murumdev, Rajgad was renamed and rebuilt by Shivaji Maharaj in 1647 as the seat of his nascent Swarajya. He lived here for 26 years and orchestrated key Maratha campaigns from these ramparts. His son Rajaram was born here, and his wife Saibai breathed her last on this fort. The capital later shifted to Raigad in 1670.',
    architecture: 'Massive complex spread across three machis (plateaus) — Padmavati, Sanjeevani and Suvela — and a central balekilla. Features include the Padmavati temple, sprawling water cisterns, gunpowder magazines, secret escape routes, and the famous Chor Darwaja (thief gate).',
    strategic: 'Commanded views of the Bhor and Velhe valleys, allowing the Marathas to monitor enemy movements deep into the Deccan. Its three-fold extension made it nearly impregnable.',
    notes: 'A challenging 4-5 hour trek from Gunjavane base village. Carry torches if planning to stay overnight in the caves. Beautiful sunsets from Suvela Machi.'
  },
  {
    id: 'raigad', name: 'Raigad Fort', district: 'Raigad', type: 'Hill Fort',
    difficulty: 'Moderate', elevation: 820, season: 'Winter, Monsoon',
    water: 'Year-round', accommodation: 'Guesthouse',
    coordinates: { lat: 18.2335, lng: 73.4400 },
    image: 'https://images.pexels.com/photos/4481330/pexels-photo-4481330.jpeg',
    summary: 'Capital of the Maratha Empire and the site of Shivaji Maharaj\u2019s coronation in 1674.',
    history: 'Originally called Rairi, this fort was captured from the Chandrarao Mores in 1656 and transformed into the Maratha capital. On 6 June 1674, Shivaji Maharaj was crowned Chhatrapati here in a grand ceremony. He passed away on the fort on 3 April 1680. His samadhi is a place of deep reverence.',
    architecture: 'Features the Maha Darwaja (Great Gate), the royal court Nagarkhana, the king\u2019s palace, the queens\u2019 quarters (Rani Vasa), Jagadishwar Temple, Hirakani Buruj and a 1737-step approach. A modern ropeway also connects the base to the top.',
    strategic: 'Naturally fortified plateau 820m above sea level, with sheer cliffs on most sides, making it almost impossible to siege.',
    notes: 'Ropeway available for non-trekkers. A guided heritage walk is highly recommended. Carry sufficient water during summers.'
  },
  {
    id: 'sinhagad', name: 'Sinhagad Fort', district: 'Pune', type: 'Hill Fort',
    difficulty: 'Easy', elevation: 1312, season: 'Monsoon, Winter',
    water: 'Year-round', accommodation: 'None',
    coordinates: { lat: 18.3664, lng: 73.7556 },
    image: 'https://images.pexels.com/photos/30308324/pexels-photo-30308324.jpeg',
    summary: 'Site of the legendary 1670 battle where Tanaji Malusare laid down his life to recapture the fort.',
    history: 'Originally known as Kondhana, the fort was held by the Mughals when Shivaji Maharaj resolved to take it back. Tanaji Malusare led a daring night assault, scaled the cliffs with the help of a monitor lizard named Yashwanti and reclaimed Kondhana. He died in battle, prompting Shivaji\u2019s famous lament: "Gad ala pan Sinh gela" (The fort is won but the lion is lost). The fort was renamed Sinhagad in his honour.',
    architecture: 'Two main gates — Pune Darwaja and Kalyan Darwaja — Tanaji\u2019s memorial, Rajaram\u2019s samadhi, Amruteshwar temple, and Dev Take water cistern.',
    strategic: 'Twin peak overlooking Pune; controlled trade routes between Konkan and Desh.',
    notes: 'Most popular weekend trek near Pune. Famous for pithla-bhakri stalls on top. Reachable by road as well.'
  },
  {
    id: 'pratapgad', name: 'Pratapgad Fort', district: 'Satara', type: 'Hill Fort',
    difficulty: 'Easy', elevation: 1080, season: 'Monsoon, Winter',
    water: 'Year-round', accommodation: 'Hotels nearby',
    coordinates: { lat: 17.9355, lng: 73.5783 },
    image: 'https://images.pexels.com/photos/37560984/pexels-photo-37560984.jpeg',
    summary: 'Witness of the historic 1659 encounter between Shivaji Maharaj and Bijapuri general Afzal Khan.',
    history: 'Built in 1656 by Moropant Trimbak Pingle. On 10 November 1659, Shivaji Maharaj famously slew Afzal Khan at the foot of this fort using the wagh nakh (tiger claws), turning the tide of the war against Bijapur. The Bhavani temple here was consecrated by Shivaji himself.',
    architecture: 'Lower fort houses the Bhavani temple and Afzal Khan\u2019s tomb at the base; upper fort has the king\u2019s residence, Maha Darwaja and bastions. A 17ft equestrian statue of Shivaji Maharaj stands atop.',
    strategic: 'Guards the Par Pass between Konkan and Desh — a vital trade and military corridor.',
    notes: 'Easily reachable by road from Mahabaleshwar (~24 km). One of the most visited Maratha heritage sites.'
  },
  {
    id: 'torna', name: 'Torna Fort', district: 'Pune', type: 'Hill Fort',
    difficulty: 'Hard', elevation: 1403, season: 'Winter',
    water: 'Seasonal', accommodation: 'Caves',
    coordinates: { lat: 18.2769, lng: 73.6228 },
    image: 'https://images.unsplash.com/photo-1660269040593-63eb316ac8d2',
    summary: 'First fort captured by 16-year-old Shivaji Maharaj in 1646, marking the dawn of Swarajya.',
    history: 'Originally a Shaiva yogi outpost, Torna was the first stronghold seized by a young Shivaji in 1646, kickstarting his dream of Hindavi Swarajya. He renamed it Prachandagad due to its formidable size.',
    architecture: 'Largest hill fort in Pune district with the Budhla Machi, Zunjar Machi, Konkan Darwaja and Menghai Devi temple. Has water tanks carved out of the rock.',
    strategic: 'Highest peak in Pune district; its sight-line spans Rajgad, Sinhagad and the Velhe valley.',
    notes: 'Challenging steep trek with rock patches. Best done with experienced trekkers. Stunning monsoon views.'
  },
  {
    id: 'lohagad', name: 'Lohagad Fort', district: 'Pune', type: 'Hill Fort',
    difficulty: 'Easy', elevation: 1033, season: 'Monsoon',
    water: 'Year-round', accommodation: 'None',
    coordinates: { lat: 18.7102, lng: 73.4847 },
    image: 'https://images.pexels.com/photos/12931217/pexels-photo-12931217.jpeg',
    summary: 'The Iron Fort \u2014 famous for its Vinchu Kata (scorpion tail) ridge and monsoon waterfalls.',
    history: 'Existed since the Satavahana period. Captured by Shivaji Maharaj in 1648, returned to the Mughals via the Treaty of Purandar and recaptured in 1670. Used by Shivaji to safely store treasures looted from Surat.',
    architecture: 'Four mighty gates \u2014 Ganesh, Narayan, Hanuman and Maha Darwaja \u2014 lead to the top. The signature feature is the Vinchu Kata, a long narrow ridge resembling a scorpion\u2019s tail.',
    strategic: 'Guards the Bhor Ghat trade route along with neighbouring Visapur fort.',
    notes: 'One of the most beginner-friendly treks. Easily accessible from Malavli railway station. Spectacular during monsoon.'
  },
  {
    id: 'shivneri', name: 'Shivneri Fort', district: 'Pune', type: 'Hill Fort',
    difficulty: 'Easy', elevation: 1006, season: 'Winter, Monsoon',
    water: 'Year-round', accommodation: 'Hotels nearby',
    coordinates: { lat: 19.2058, lng: 73.8511 },
    image: 'https://images.unsplash.com/photo-1594547121826-3445761d2ce5',
    summary: 'Birthplace of Chhatrapati Shivaji Maharaj, born here on 19 February 1630.',
    history: 'A 6th-century fort that gained renewed importance when Shivaji Maharaj was born here to Shahaji Bhosale and Jijabai. Jijabai chose Shivneri for safety during turbulent times. Shivaji spent his early years here learning the basics of warfare.',
    architecture: 'Seven successive gateways, the Shivai Devi temple after which Shivaji was named, the Shivkunj birthplace memorial, Badami Talav and Ganga-Jamuna water tanks.',
    strategic: 'Overlooks the Naneghat pass, an ancient trade route between Konkan and Junnar.',
    notes: 'Located near Junnar town. ASI protected monument. Best visited with the nearby Lenyadri Ashtavinayak temple.'
  },
  {
    id: 'harishchandragad', name: 'Harishchandragad Fort', district: 'Ahmednagar', type: 'Hill Fort',
    difficulty: 'Hard', elevation: 1424, season: 'Winter, Monsoon',
    water: 'Year-round', accommodation: 'Caves',
    coordinates: { lat: 19.3866, lng: 73.7770 },
    image: 'https://images.pexels.com/photos/14229957/pexels-photo-14229957.jpeg',
    summary: 'Ancient fort famous for the spectacular cliff of Konkan Kada \u2014 a near-vertical 1700ft drop.',
    history: 'Dates back to the 6th century during the Kalachuri dynasty, with caves and temples built between the 11th and 13th centuries during the Yadava reign. Mentioned in Matsyapurana and Skandapurana.',
    architecture: 'Harishchandreshwar temple carved out of a single rock, Kedareshwar cave with a giant Shivling submerged in water, Taramati peak (1429m), and the iconic concave Konkan Kada cliff.',
    strategic: 'Guarded the Malshej corridor between Konkan and the Deccan plateau.',
    notes: 'Multiple trek routes \u2014 Khireshwar (easiest), Pachnai (moderate) and Nalichi Vaat (extreme). Camp overnight to catch the sunrise from Konkan Kada.'
  },
  {
    id: 'murud-janjira', name: 'Murud-Janjira Fort', district: 'Raigad', type: 'Sea Fort',
    difficulty: 'Easy', elevation: 0, season: 'Winter',
    water: 'Sea around', accommodation: 'Hotels in Murud',
    coordinates: { lat: 18.2997, lng: 72.9644 },
    image: 'https://images.pexels.com/photos/30308324/pexels-photo-30308324.jpeg',
    summary: 'The undefeated sea fort of the Siddis \u2014 never breached by Marathas, Portuguese or British.',
    history: 'Built in the late 15th century by the Nizamshahi sultans and strengthened by the Siddis of Janjira, the fort resisted repeated Maratha sieges, including those led by Shivaji and Sambhaji. Sambhaji famously tried to cut a tunnel under the sea to breach it.',
    architecture: 'Oval fort spread over 22 acres rising directly from the Arabian Sea. 19 bastions, three massive cannons named Kalal Bangadi, Chavri and Landa Kasam. Freshwater lakes inside the saline-water fort.',
    strategic: 'Almost impregnable due to its location on a rocky islet \u2014 only reachable by boat.',
    notes: 'Reach by sailboat from Rajapuri jetty. Boats operate only in fair sea conditions, generally October to May.'
  },
  {
    id: 'vijaydurg', name: 'Vijaydurg Fort', district: 'Sindhudurg', type: 'Sea Fort',
    difficulty: 'Easy', elevation: 0, season: 'Winter',
    water: 'Sea around', accommodation: 'Hotels nearby',
    coordinates: { lat: 16.5616, lng: 73.3361 },
    image: 'https://images.unsplash.com/photo-1660269040593-63eb316ac8d2',
    summary: 'Gibraltar of the East \u2014 Maratha naval headquarters fortified by Shivaji and Kanhoji Angre.',
    history: 'Built in 1193 by Raja Bhoja II and captured by Shivaji Maharaj in 1653. Renamed Vijaydurg (Fort of Victory). Later it became the formidable base of Maratha admiral Kanhoji Angre, who terrorised European fleets in the Arabian Sea.',
    architecture: 'Three layers of fortification, 27 bastions, an underwater wall that wrecked enemy ships, secret tunnels and a dry-dock for ship-building.',
    strategic: 'Natural harbour and deep waters of the Waghotan creek made it an ideal naval base.',
    notes: 'Reachable by road from Devgad. Combine your visit with Sindhudurg fort for a coastal heritage tour.'
  },
  {
    id: 'sindhudurg', name: 'Sindhudurg Fort', district: 'Sindhudurg', type: 'Sea Fort',
    difficulty: 'Easy', elevation: 0, season: 'Winter',
    water: 'Sea around', accommodation: 'Hotels in Malvan',
    coordinates: { lat: 16.0383, lng: 73.4569 },
    image: 'https://images.pexels.com/photos/4481330/pexels-photo-4481330.jpeg',
    summary: 'Island fortress off the Malvan coast \u2014 home to the only temple of Shivaji Maharaj as a deity.',
    history: 'Construction began on 25 November 1664 under the supervision of Hiroji Indulkar. Built with 4000 mounds of iron and 2000 Khandis of lime mixed with sand and lead. It served as a key Maratha naval base.',
    architecture: 'Spread over 48 acres on the rocky islet of Kurte. Has 42 bastions, freshwater wells inside saline surroundings, an imprint of Shivaji\u2019s palm and foot in lime mortar, and the unique Shivrajeshwar temple.',
    strategic: 'Defended the western coastline of Maharashtra against the Portuguese, Dutch and English.',
    notes: 'Famous Malvani cuisine in the nearby town. Boat ride from Malvan jetty is mandatory.'
  },
  {
    id: 'panhala', name: 'Panhala Fort', district: 'Kolhapur', type: 'Hill Fort',
    difficulty: 'Easy', elevation: 845, season: 'All seasons',
    water: 'Year-round', accommodation: 'Hotels on fort',
    coordinates: { lat: 16.8127, lng: 74.1106 },
    image: 'https://images.unsplash.com/photo-1491497895121-1334fc14d8c9',
    summary: 'One of the largest forts in the Deccan and home to Tarabai\u2019s heroic regency.',
    history: 'Built by Bhoja II of the Shilahara dynasty between 1178\u20131209. Came under the Marathas in 1659. Site of the dramatic 1660 escape of Shivaji Maharaj from the Bijapuri siege, made possible by the supreme sacrifice of Baji Prabhu Deshpande at Pavan Khind. Later, Tarabai ruled the Maratha Empire from here.',
    architecture: 'Three impressive double-gates \u2014 Char Darwaja, Teen Darwaja and Wagh Darwaja. Sajja Kothi (royal lookout), Andhar Bavadi (hidden stepwell) and the massive Ambarkhana granary.',
    strategic: 'Sprawls over 14 km of fortification \u2014 one of the largest in the Deccan.',
    notes: 'Connected by road. Pair with a visit to Pavan Khind \u2014 a 12km drive from the fort.'
  },
  {
    id: 'visapur', name: 'Visapur Fort', district: 'Pune', type: 'Hill Fort',
    difficulty: 'Moderate', elevation: 1084, season: 'Monsoon',
    water: 'Seasonal', accommodation: 'None',
    coordinates: { lat: 18.7333, lng: 73.4833 },
    image: 'https://images.pexels.com/photos/12931217/pexels-photo-12931217.jpeg',
    summary: 'Twin of Lohagad \u2014 a Peshwa-era fort with grand cliff-side waterfalls in monsoon.',
    history: 'Built between 1713 and 1720 by Balaji Vishwanath, the first Peshwa. Considered superior to Lohagad in strategic terms.',
    architecture: 'Larger plateau than Lohagad, large carved Hanuman idol on the rock face, water cisterns and ruined cannon emplacements.',
    strategic: 'Provided artillery cover for the lower Lohagad fort.',
    notes: 'Trek can be slippery in monsoon. Approach via Bhaje village. Bhaje caves nearby make a great combo trip.'
  },
  {
    id: 'tikona', name: 'Tikona Fort', district: 'Pune', type: 'Hill Fort',
    difficulty: 'Easy', elevation: 1100, season: 'Monsoon, Winter',
    water: 'Year-round', accommodation: 'None',
    coordinates: { lat: 18.6444, lng: 73.5111 },
    image: 'https://images.unsplash.com/photo-1594547121826-3445761d2ce5',
    summary: 'Triangular pyramid-shaped fort overlooking the Pavna reservoir.',
    history: 'Captured by Shivaji Maharaj in 1657 from Adil Shahi rule. Later transferred to the Mughals via the Treaty of Purandar and reclaimed in 1670.',
    architecture: 'Steep triangular structure with seven water cisterns, a Trimbakeshwar Mahadev cave temple and ruined ramparts.',
    strategic: 'Watch-fort for the Mawal region; pairs with Tung fort across the Pavna lake.',
    notes: 'Quick 1.5-hour trek. Excellent views of Tung, Lohagad and Pavna backwaters.'
  },
  {
    id: 'tung', name: 'Tung Fort', district: 'Pune', type: 'Hill Fort',
    difficulty: 'Moderate', elevation: 1075, season: 'Monsoon, Winter',
    water: 'Seasonal', accommodation: 'None',
    coordinates: { lat: 18.6650, lng: 73.5050 },
    image: 'https://images.pexels.com/photos/4481330/pexels-photo-4481330.jpeg',
    summary: 'Also known as Kathingad \u2014 a steep watch-fort guarding the Pavna lake region.',
    history: 'Pre-Maratha fort which came under Shivaji Maharaj in 1657 as part of his Konkan campaign.',
    architecture: 'Conical narrow summit with Tunga Devi temple, Ganesh temple and ruined fortification walls.',
    strategic: 'Used as a lookout fort due to its sharp gradient and panoramic view.',
    notes: 'Steep climb in the last section. Boat ride across Pavna lake adds to the experience.'
  },
  {
    id: 'korigad', name: 'Korigad Fort', district: 'Pune', type: 'Hill Fort',
    difficulty: 'Easy', elevation: 923, season: 'Monsoon, Winter',
    water: 'Year-round', accommodation: 'Resorts at base',
    coordinates: { lat: 18.6928, lng: 73.4275 },
    image: 'https://images.unsplash.com/photo-1660269040593-63eb316ac8d2',
    summary: 'A flat-topped fort near Lonavla, famous for its intact ramparts and Koraidevi temple.',
    history: 'Existed before 1500 CE; captured by Shivaji Maharaj in 1657 and remained in Maratha hands until 1818, when the British finally took it after intense shelling.',
    architecture: 'Almost intact fortified wall encircling the plateau, six water tanks, six cannons, Koraidevi and Vishnu temples.',
    strategic: 'Defended the Aamby Valley region and the western approaches to the Sahyadris.',
    notes: 'Great family-friendly trek. Often combined with the Aamby Valley drive.'
  },
  {
    id: 'rajmachi', name: 'Rajmachi Fort', district: 'Raigad', type: 'Hill Fort',
    difficulty: 'Moderate', elevation: 826, season: 'Monsoon',
    water: 'Year-round', accommodation: 'Homestay at base village',
    coordinates: { lat: 18.8255, lng: 73.4133 },
    image: 'https://images.pexels.com/photos/12931217/pexels-photo-12931217.jpeg',
    summary: 'Twin forts Shrivardhan and Manaranjan, with the picturesque Udhewadi village in between.',
    history: 'Built during the Satavahana era; came under Shivaji Maharaj after 1657. Bajirao I used it to plan the Bassein campaign against the Portuguese.',
    architecture: 'Two-fort complex \u2014 Shrivardhan (larger) and Manaranjan (older) \u2014 connected by a saddle. Carved water tanks, Bhairavnath temple and old stone houses.',
    strategic: 'Watch over the Bor Pass and the trade caravan route from Pune to Mumbai.',
    notes: 'Spectacular monsoon trek from Kondivade or via Lonavla. Fireflies festival nearby in May.'
  },
  {
    id: 'kalavantin', name: 'Kalavantin Durg', district: 'Raigad', type: 'Hill Fort',
    difficulty: 'Hard', elevation: 686, season: 'Winter',
    water: 'Seasonal', accommodation: 'None',
    coordinates: { lat: 18.8650, lng: 73.1989 },
    image: 'https://images.pexels.com/photos/30308324/pexels-photo-30308324.jpeg',
    summary: 'A near-vertical thumb-shaped pinnacle with hand-carved steps cut into bare rock.',
    history: 'Lore says it was built for an ancient queen Kalavantin during the Yadava era. Its real history is sparse, but it served as a sentinel for the Prabalgad complex.',
    architecture: 'No fortifications on top \u2014 just a small plateau. The unique feature is the exposed rock-cut staircase with no railings.',
    strategic: 'Lookout point providing visibility over the Konkan region.',
    notes: 'Not for beginners or those with vertigo. Pair with the adjacent Prabalgad trek.'
  },
  {
    id: 'karnala', name: 'Karnala Fort', district: 'Raigad', type: 'Hill Fort',
    difficulty: 'Easy', elevation: 475, season: 'Monsoon, Winter',
    water: 'Seasonal', accommodation: 'Hotels nearby',
    coordinates: { lat: 18.8867, lng: 73.1133 },
    image: 'https://images.unsplash.com/photo-1594547121826-3445761d2ce5',
    summary: 'A funnel-shaped basalt pillar fort inside the Karnala Bird Sanctuary.',
    history: 'Built by the Devagiri Yadavas in the 13th century. Changed hands between Tughluqs, Nizam Shah, Portuguese, Marathas and finally the British in 1818.',
    architecture: 'Distinctive thumb-shaped rock pinnacle ("Funnel Hill") rising 125ft above the upper fort, twin water cisterns, multiple bastions.',
    strategic: 'Controlled the Bhor Ghat traffic from Mumbai to Pune.',
    notes: 'Easy 2-hour trek with great bird-watching opportunities. Located right off the Mumbai-Goa highway.'
  },
  {
    id: 'mahuli', name: 'Mahuli Fort', district: 'Thane', type: 'Hill Fort',
    difficulty: 'Hard', elevation: 815, season: 'Monsoon, Winter',
    water: 'Seasonal', accommodation: 'None',
    coordinates: { lat: 19.4500, lng: 73.2667 },
    image: 'https://images.unsplash.com/photo-1491497895121-1334fc14d8c9',
    summary: 'Highest peak in Thane district \u2014 a sprawling three-fort complex.',
    history: 'Existed since the time of Aurangzeb\u2019s ancestor Murtaza Nizam Shah. Captured by Shivaji Maharaj in 1658, lost in 1661 and reclaimed in 1670 via the Treaty of Purandar reversal.',
    architecture: 'Three connected peaks \u2014 Mahuli, Bhandargad and Palasgad \u2014 with ruined gates, cisterns and a Shiva temple atop.',
    strategic: 'Strategic watch-fort for north Konkan and the Tansa valley.',
    notes: 'Rocky and steep \u2014 includes a famous iron ladder section. Take an experienced guide for the final pinnacle.'
  },
  {
    id: 'salher', name: 'Salher Fort', district: 'Nashik', type: 'Hill Fort',
    difficulty: 'Hard', elevation: 1567, season: 'Winter',
    water: 'Year-round', accommodation: 'Caves',
    coordinates: { lat: 20.7333, lng: 73.9333 },
    image: 'https://images.pexels.com/photos/14229957/pexels-photo-14229957.jpeg',
    summary: 'Highest fort in Maharashtra and site of the decisive 1672 Maratha victory over the Mughals.',
    history: 'Captured by Shivaji Maharaj in 1671. The battle of Salher in 1672 was the first open-ground Maratha victory against the Mughals, where Suryaji Kakade and Pratapraoji Gujjar defeated a 40,000-strong Mughal army.',
    architecture: 'Twin peaks (Salher & Salota) connected by a saddle, ten gates, ruined palaces, Parashuram temple and large water tanks. Highest point in Sahyadri.',
    strategic: 'Commanded the Baglan region near the Gujarat-Maharashtra border.',
    notes: 'Long, challenging trek from Waghambe village. Pair with Mulher fort. Best done in November-February.'
  },
  {
    id: 'ratangad', name: 'Ratangad Fort', district: 'Ahmednagar', type: 'Hill Fort',
    difficulty: 'Moderate', elevation: 1297, season: 'Monsoon, Winter',
    water: 'Year-round', accommodation: 'Caves',
    coordinates: { lat: 19.5483, lng: 73.7039 },
    image: 'https://images.pexels.com/photos/4481330/pexels-photo-4481330.jpeg',
    summary: 'The Jewel Fort \u2014 home to the iconic natural rock hole \u2018Nedhe\u2019.',
    history: 'Said to be over 400 years old, captured by Shivaji Maharaj in 1657. Used as a watch-tower for the Bhandardara region.',
    architecture: 'Four gates \u2014 Ganesh, Hanuman, Konkan and Trimbak \u2014 the Nedhe (natural rock window), and ruined bastions.',
    strategic: 'Commanding views of Kalsubai (highest peak in Maharashtra) and the Pravara valley.',
    notes: 'Beautiful monsoon trek from Ratanwadi village, near the famous Amruteshwar temple.'
  },
  {
    id: 'alibaug', name: 'Kolaba Fort', district: 'Raigad', type: 'Sea Fort',
    difficulty: 'Easy', elevation: 0, season: 'Winter',
    water: 'Sea around', accommodation: 'Hotels in Alibaug',
    coordinates: { lat: 18.6411, lng: 72.8633 },
    image: 'https://images.unsplash.com/photo-1660269040593-63eb316ac8d2',
    summary: 'Tidal sea-fort at Alibaug \u2014 walk to it at low tide, sail across at high tide.',
    history: 'Strengthened by Shivaji Maharaj in 1662 as a Maratha naval base. Sambhaji Maharaj built the Maha Darwaja in 1681. Sarkhel Kanhoji Angre used it as his eastern naval HQ.',
    architecture: 'Two main gates, freshwater wells inside saline surroundings, Ganesh temple, large bastions and rusted cannons.',
    strategic: 'Defended the northern Konkan coast and Bombay harbour approaches.',
    notes: 'Walk to the fort at low tide. Famous Hirakot Lake and Alibaug beach nearby.'
  },
  {
    id: 'daulatabad', name: 'Daulatabad Fort', district: 'Aurangabad', type: 'Hill Fort',
    difficulty: 'Easy', elevation: 200, season: 'Winter',
    water: 'Seasonal', accommodation: 'Hotels in Aurangabad',
    coordinates: { lat: 19.9433, lng: 75.2167 },
    image: 'https://images.unsplash.com/photo-1594547121826-3445761d2ce5',
    summary: 'Devagiri \u2014 a 12th-century fort that briefly became Tughlaq\u2019s capital of India.',
    history: 'Built by the Yadavas of Devagiri in the 12th century. In 1327, Muhammad bin Tughluq forcibly relocated Delhi\u2019s entire population here and renamed it Daulatabad. The disastrous experiment was abandoned within a few years.',
    architecture: 'Conical hill with a vertical scarp, a dark winding tunnel as the only access, the Chand Minar (a 30m tall victory tower built in 1435) and the Chini Mahal.',
    strategic: 'Considered one of the strongest forts of medieval India \u2014 the moat and tunnel made it nearly impregnable.',
    notes: 'A short drive from Ellora caves. Carry a torch to navigate the dark tunnel.'
  },
  {
    id: 'janjira-revas', name: 'Padmadurg Fort', district: 'Raigad', type: 'Sea Fort',
    difficulty: 'Easy', elevation: 0, season: 'Winter',
    water: 'Sea around', accommodation: 'Hotels in Murud',
    coordinates: { lat: 18.3083, lng: 72.9583 },
    image: 'https://images.pexels.com/photos/4481330/pexels-photo-4481330.jpeg',
    summary: 'Sea-fort built by Shivaji Maharaj to counter the unyielding Janjira Siddis.',
    history: 'Construction began in 1672 by Shivaji Maharaj on the rocky island of Kasa, just opposite Janjira. Intended as a launchpad to besiege Murud-Janjira from sea.',
    architecture: 'Stone fortification with a Padmavati temple and remains of the old Maratha navy quarters. Some portions have been eroded by the sea.',
    strategic: 'A bold offensive base meant to project Maratha sea-power against the Siddis.',
    notes: 'Boats from Murud-Janjira jetty. Visit only when the sea is calm.'
  },
  {
    id: 'devgad', name: 'Devgad Fort', district: 'Sindhudurg', type: 'Sea Fort',
    difficulty: 'Easy', elevation: 50, season: 'Winter',
    water: 'Sea around', accommodation: 'Hotels nearby',
    coordinates: { lat: 16.3833, lng: 73.3833 },
    image: 'https://images.unsplash.com/photo-1491497895121-1334fc14d8c9',
    summary: 'Coastal fortress famous for the adjacent Devgad lighthouse and Alphonso mango farms.',
    history: 'Built by Shivaji Maharaj in 1670 as part of his Konkan coastal defence chain.',
    architecture: 'Triangular fort with ten bastions, cannons, freshwater well and a modern lighthouse adjacent to the fort.',
    strategic: 'Guarded the southern Konkan coastal trade route.',
    notes: 'Easy walk-up; combine with the famous Devgad windmill view-point and mango orchards in season.'
  },
  {
    id: 'kalavanti-prabal', name: 'Prabalgad Fort', district: 'Raigad', type: 'Hill Fort',
    difficulty: 'Hard', elevation: 707, season: 'Winter',
    water: 'Seasonal', accommodation: 'None',
    coordinates: { lat: 18.8650, lng: 73.2050 },
    image: 'https://images.pexels.com/photos/30308324/pexels-photo-30308324.jpeg',
    summary: 'Mighty plateau fort beside Kalavantin Durg, also known as Muranjan.',
    history: 'Pre-Maratha fort that came to Shivaji Maharaj in 1657. Heavily fortified by the Marathas.',
    architecture: 'Sprawling flat plateau with dense vegetation, ruined temples, fortified gates and a hidden cave.',
    strategic: 'Watched over the Panvel and Karnala routes towards Mumbai.',
    notes: 'Often climbed in combination with Kalavantin Durg. Beware of dense undergrowth and snakes in monsoon.'
  },
  {
    id: 'naldurg', name: 'Naldurg Fort', district: 'Osmanabad', type: 'Land Fort',
    difficulty: 'Easy', elevation: 600, season: 'Winter',
    water: 'Year-round', accommodation: 'Hotels in Solapur',
    coordinates: { lat: 17.8167, lng: 76.2833 },
    image: 'https://images.pexels.com/photos/37560984/pexels-photo-37560984.jpeg',
    summary: 'A massive land fort with the spectacular \u2018Pani Mahal\u2019 \u2014 a palace built inside a dam.',
    history: 'Built by the Chalukyas, fortified by the Bahamanis and finally the Adilshahis. Notable feature: the dam-bridge across the Bori river with a palace inside it built by Ibrahim Adil Shah II in the 17th century.',
    architecture: 'Sprawling complex with 114 bastions, the Upali Buruj (highest bastion), the unique Pani Mahal water-palace and twin moats.',
    strategic: 'Key border fort between the Bahamani and Vijayanagara empires.',
    notes: 'Bus accessible. Best appreciated during a guided heritage walk.'
  },
  {
    id: 'ahmednagar', name: 'Ahmednagar Fort', district: 'Ahmednagar', type: 'Land Fort',
    difficulty: 'Easy', elevation: 658, season: 'Winter',
    water: 'Year-round', accommodation: 'Hotels in Ahmednagar',
    coordinates: { lat: 19.0917, lng: 74.7333 },
    image: 'https://images.unsplash.com/photo-1660269040593-63eb316ac8d2',
    summary: 'A perfectly oval fort that imprisoned Pandit Nehru during the Quit India Movement.',
    history: 'Built in 1490 by Ahmad Nizam Shah I, founder of the Nizam Shahi dynasty. The British later used its rooms to imprison Jawaharlal Nehru, Abul Kalam Azad and other Congress leaders from 1942-45, where Nehru wrote \u2018The Discovery of India\u2019.',
    architecture: 'Almost perfect oval with 24 bastions, a wide moat and the famed Hindola or Hanging Gateway.',
    strategic: 'Capital fortress of the Nizam Shahi dynasty.',
    notes: 'Today an army cantonment. Limited access \u2014 prior permission required.'
  },
  {
    id: 'kalsubai', name: 'Bitangad Fort', district: 'Ahmednagar', type: 'Hill Fort',
    difficulty: 'Moderate', elevation: 938, season: 'Monsoon, Winter',
    water: 'Seasonal', accommodation: 'Homestay at base',
    coordinates: { lat: 19.5478, lng: 73.7050 },
    image: 'https://images.unsplash.com/photo-1594547121826-3445761d2ce5',
    summary: 'A lesser-known fort with a distinctive thumb-shaped pinnacle near Bhandardara.',
    history: 'Believed to be built by the Yadavas. Came under Maratha control and later the Mughals.',
    architecture: 'Steep rock-cut steps to a small summit with three water tanks and a Bhairavnath temple.',
    strategic: 'Watch-fort for the Pravara valley.',
    notes: 'Quiet weekend trek with stunning monsoon views of Kalsubai peak.'
  }
];

export function getFortById(id) {
  return FORTS.find(f => f.id === id);
}

export function listDistricts() {
  return Array.from(new Set(FORTS.map(f => f.district))).sort();
}

export function listTypes() {
  return Array.from(new Set(FORTS.map(f => f.type))).sort();
}

export function listDifficulties() {
  return ['Easy', 'Moderate', 'Hard'];
}

export function listSeasons() {
  const all = FORTS.flatMap(f => f.season.split(',').map(s => s.trim()));
  return Array.from(new Set(all)).sort();
}
