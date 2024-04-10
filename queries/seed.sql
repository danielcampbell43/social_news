INSERT INTO stories (score, title, URL)
VALUES (43, 'Voters Overwhelmingly Back Community Broadband in Chicago and Denver', 'https://www.vice.com/en/article/xgzxvz/voters-overwhelmingly-back-community-broadband-in-chicago-and-denver')
     , (24, 'eBird: A crowdsourced bird sighting database', 'https://ebird.org/home')
     , (471, 'Karen Gillan teams up with Lena Headey and Michelle Yeoh in assassin thriller Gunpowder Milkshake', 'https://www.empireonline.com/movies/news/gunpowder-milk-shake-lena-headey-karen-gillan-exclusive/')
     , (101, 'Pfizers coronavirus vaccine is more than 90 percent effective in first analysis, company reports', 'https://www.cnbc.com/2020/11/09/covid-vaccine-pfizer-drug-is-more-than-90percent-effective-in-preventing-infection.html')
     , (87, 'Budget: Pensions to get boost as tax-free limit to rise', 'https://www.bbc.co.uk/news/business-64949083')
     , (0, 'Ukraine war: Zelensky honours unarmed soldier filmed being shot', 'https://www.bbc.co.uk/news/world-europe-64938934')
     , (2, 'SVB and Signature Bank: How bad is US banking crisis and what does it mean?', 'https://www.bbc.co.uk/news/business-64951630')
     , (131, 'Aukus deal: Summit was projection of power and collaborative intent', 'https://www.bbc.co.uk/news/uk-politics-64948535')
     , (42,'Dancer whose barefoot video went viral meets Camilla', 'https://www.bbc.co.uk/news/uk-england-birmingham-64953863');

ALTER TABLE stories 
DROP COLUMN score;