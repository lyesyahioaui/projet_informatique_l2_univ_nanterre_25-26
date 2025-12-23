DROP TABLE IF EXISTS  observe_nichoir CASCADE;
DROP TABLE IF EXISTS anime CASCADE;
DROP TABLE IF EXISTS observe CASCADE;
DROP TABLE IF EXISTS possede CASCADE;
DROP TABLE IF EXISTS regarder CASCADE;
DROP TABLE IF EXISTS specialisation CASCADE;
DROP TABLE IF EXISTS paye CASCADE;
DROP TABLE IF EXISTS inscrit CASCADE;
DROP TABLE IF EXISTS especes CASCADE;
DROP TABLE IF EXISTS groupe_espece CASCADE;
DROP TABLE IF EXISTS caracteristique CASCADE;
DROP TABLE IF EXISTS status CASCADE;
DROP TABLE IF EXISTS cotisation CASCADE;
DROP TABLE IF EXISTS adherent CASCADE;
DROP TABLE IF EXISTS animateur CASCADE;
DROP TABLE IF EXISTS sortie CASCADE;
DROP TABLE IF EXISTS nichoir CASCADE;
DROP TABLE If EXISTS gestionnaire CASCADE;

CREATE TABLE sortie (
    id_sortie SERIAL PRIMARY KEY,
    theme VARCHAR(100) NOT NULL,
    lieu_rdv VARCHAR(100) NOT NULL,
    date_rdv TIMESTAMP NOT NULL,
    dparcours INTEGER CHECK (dparcours > 0),
    effectif_max INTEGER CHECK (effectif_max > 0)
);

CREATE TABLE adherent (
    id_adh SERIAL PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    adr_mail VARCHAR(100) UNIQUE NOT NULL,
    num_phone VARCHAR(20) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(20) UNIQUE NOT NULL,
    est_gestionnaire BOOLEAN DEFAULT FALSE
);
CREATE TABLE gestionnaire (
    id_gestionnaire INTEGER NOT NULL UNIQUE REFERENCES adherent(id_adh) ON DELETE CASCADE ON UPDATE CASCADE 
);



CREATE TABLE cotisation (
    id_cot SERIAL PRIMARY KEY,
    prix FLOAT CHECK (prix > 0)
);

CREATE TABLE status (
    id_status SERIAL PRIMARY KEY,
    nom_status VARCHAR(300) UNIQUE NOT NULL
);

CREATE TABLE caracteristique (
    idc SERIAL PRIMARY KEY,
    characteristique VARCHAR(300) UNIQUE NOT NULL
);

CREATE TABLE groupe_espece (
    idge SERIAL PRIMARY KEY,
    nomge VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE especes (
    id_especes SERIAL PRIMARY KEY,
    nom VARCHAR(50) UNIQUE NOT NULL,
    idge INTEGER REFERENCES groupe_espece(idge) ON DELETE SET NULL ON UPDATE CASCADE
);


CREATE TABLE possede (
    idge INTEGER REFERENCES groupe_espece(idge) ON DELETE CASCADE ON UPDATE CASCADE,
    id_especes INTEGER REFERENCES especes(id_especes) ON DELETE CASCADE ON UPDATE CASCADE,
    idc INTEGER REFERENCES caracteristique(idc) ON DELETE CASCADE ON UPDATE CASCADE,
    valeur INTEGER CHECK (valeur >= 0),
    PRIMARY KEY (idge, id_especes, idc)
);

CREATE TABLE nichoir (
    idn SERIAL PRIMARY KEY,
    date_inst DATE NOT NULL,
    lieu_inst VARCHAR(100) NOT NULL
);

CREATE TABLE observe_nichoir (
    idon SERIAL ,
    nbr_oeuf INTEGER CHECK (nbr_oeuf >= 0),
    type_occ VARCHAR(50) NOT NULL,
    periode_nid VARCHAR(100),
    idn INTEGER REFERENCES nichoir(idn) ON DELETE CASCADE ON UPDATE CASCADE,
    id_adh INTEGER REFERENCES adherent(id_adh) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (idon,idn,id_adh)
);

CREATE TABLE anime (
    id_adh INTEGER REFERENCES adherent(id_adh) ON DELETE CASCADE ON UPDATE CASCADE,
    id_sortie INTEGER REFERENCES sortie(id_sortie) ON DELETE CASCADE ON UPDATE CASCADE,
    id_animateur INTEGER REFERENCES animateur(id_animateur) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (id_adh, id_sortie, id_animateur)
);

CREATE TABLE inscrit (
    id_adh INTEGER REFERENCES adherent(id_adh) ON DELETE CASCADE ON UPDATE CASCADE,
    id_sortie INTEGER REFERENCES sortie(id_sortie) ON DELETE CASCADE ON UPDATE CASCADE,
    date_s DATE NOT NULL,
    PRIMARY KEY (id_adh, id_sortie)
);

CREATE TABLE paye (
    id_adh INTEGER REFERENCES adherent(id_adh) ON DELETE CASCADE ON UPDATE CASCADE,
    id_status INTEGER REFERENCES status(id_status) ON DELETE CASCADE ON UPDATE CASCADE,
    id_cot INTEGER REFERENCES cotisation(id_cot) ON DELETE CASCADE ON UPDATE CASCADE,
    moy_p VARCHAR(50) NOT NULL,
    date_pay DATE NOT NULL,
    PRIMARY KEY (id_adh, id_status, id_cot)
);

CREATE TABLE observe (
    id_adh INTEGER REFERENCES adherent(id_adh) ON DELETE CASCADE ON UPDATE CASCADE,
    id_especes INTEGER REFERENCES especes(id_especes) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (id_adh, id_especes)
);

CREATE TABLE regarder (
    idn INTEGER REFERENCES nichoir(idn) ON DELETE CASCADE ON UPDATE CASCADE,
    id_adh INTEGER REFERENCES adherent(id_adh) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (idn, id_adh)
);

CREATE TABLE specialisation (
    id_adh INTEGER REFERENCES adherent(id_adh) ON DELETE CASCADE ON UPDATE CASCADE,
    specialite VARCHAR(50) NOT NULL,
    PRIMARY KEY (id_adh, specialite)
);


---Filling table caracteristique :
INSERT INTO caracteristique(idc,caracteristique) VALUES
  	(1,'Plumage coloré'), 
  	(2,'Chant mélodieux'), 
  	(3,'Taille moyenne'), 
  	(4,'Habitat varié'), 
  	(5,'Comportement grégaire'), 
  	(6,'Nidification précoce'), 
  	(7,'Migration saisonnière'), 
  	(8,'Alimentation variée'), 
  	(9,'Espèce protégée'), 
  	(10,'Comportement territorial'), 
  	(11,'Mœurs solitaires'), 
  	(12,'Nourriture insectivore'), 
  	(13,'Nourriture granivore'), 
  	(14,'Nourriture piscivore'), 
  	(15,'Nourriture omnivore');


---Filling table groupe_espece :
 
INSERT INTO groupe_espece (idge, nomge) VALUES
(1,'Passereaux'),  
(2,'Rapaces'),     
(3,'Aquatiques'),
(4,'Migrateurs'),   
(5,'Sédentaires'),  
(6,'Insectivores'), 
(7,'Granivores'),   
(8,'Omnivores'),     
(9,'Carnivores'),    
(10,'Herbivores'),    
(11,'Nicheurs en colonies'), 
(12,'Nicheurs solitaires'),   
(13,'Espèces menacées'),     
(14,'Espèces communes'),     
(15,'Espèces endémiques');
---Filling table espece  :
INSERT INTO especes (id_especes, nome, idge) VALUES
(1,'Rouge-gorge familier', 1),   -- valeur = nombre de caractéristiques pour cette espèce
(2,'Hirondelle rustique', 2),
(3,'Mésange charbonnière', 3),
(4,'Pigeon ramier', 4),
(5,'Buse variable', 5),
(6,'Aigle royal', 6),
(7,'Faucon crécerelle', 7),
(8,'Canard colvert',8),
(9,'Cigogne blanche', 9),
(10,'Grue cendrée', 10),
(11,'Merle noir',11),
(12,'Pic vert',12),
(13,'Pie bavarde',13),
(14,'Étourneau sansonnet',14),
(15,'Serin cini',15);

---Filling table possede:
INSERT INTO possede (idge, id_especes, idc, valeur) VALUES
(1, 1, 1, 3),
(1, 1, 2, 5),
(2, 5, 9, 2),
(2, 6, 10, 4),
(3, 8, 14, 1),
(4, 2, 7, 3),
(4, 9, 7, 2),
(5, 4, 4, 4),
(6, 3, 12, 5),
(7, 15, 13, 3),
(8, 13, 15, 2),
(9, 7, 9, 4),
(10, 10, 8, 1),
(11, 14, 5, 3),
(12, 12, 11, 2);

---Filling table status :
INSERT INTO status (id_status, nom_status) VALUES
(1, 'Actif'),
(2, 'Inactif'),
(3, 'En attente'),
(4, 'Suspendu'),
(5, 'Résilié');


---Filling table cotisation :
INSERT INTO cotisation (id_cot , prix) VALUES
 (1 ,25.50),
 (2 ,30.00),
 (3 ,15.75),
 (4 ,40.20),
 (5 ,50.00),
 (6 ,60.50),
 (7 ,35.75),
 (8 ,20.00),
 (9 ,45.30),
 (10 ,55.80),
 (11 ,70.10),
 (12 ,80.25),
 (13 ,90.60),
 (14 ,100.50),
 (15 ,110.90);



---Filling table animateur :
INSERT INTO animateur (id_animateur, nom, num_phone) VALUES
(1, 'Jean Dupont', '+33 6 12 34 56 78'),
(2, 'Marie Curie', '+33 6 23 45 67 89'),
(3, 'Paul Martin', '+33 6 34 56 78 90'),
(4, 'Sophie Durand', '+33 6 45 67 89 01'),
(5, 'Lucie Bernard', '+33 6 56 78 90 12'),
(6, 'Pierre Lefèvre', '+33 6 67 89 01 23'),
(7, 'Clara Moreau', '+33 6 78 90 12 34'),
(8, 'Thomas Petit', '+33 6 89 01 23 45'),
(9, 'Emma Richard', '+33 6 90 12 34 56'),
(10, 'Lucas Simon', '+33 6 01 23 45 67'),
(11, 'Alice Garnier', '+33 6 12 34 56 78'),
(12, 'Victor Lemoine', '+33 6 23 45 67 89'),
(13, 'Chloé Fournier', '+33 6 34 56 78 90'),
(14, 'Antoine Roche', '+33 6 45 67 89 01'),
(15, 'Juliette Lambert', '+33 6 56 78 90 12');


 
---Filling table adhérent :
INSERT INTO adherent (id_adh, nom, prenom, adr_mail, num_phone, mot_de_passe, est_gestionnaire) VALUES
(1,'Martin','Alice','alice.martin@gmail.com','+33 6 11 22 33 44','martinalice44', 'False'),
(2,'Bernard','Louis','louis.bernard@gmail.com','+33 6 22 33 44 55','bernardlouis55', 'False'),
(3,'Durand','Sophie','sophie.durand@gmail.com','+33 6 33 44 55 66','durandsophie66', 'False'),
(4,'Lefèvre','Paul','paul.lefevre@gmail.com','+33 6 44 55 66 77','lefèvrepaul77', 'False'),
(5,'Moreau','Clara','clara.moreau@gmail.com','+33 6 55 66 77 88','moreauclara88', 'False'),
(6,'Petit','Thomas','thomas.petit@gmail.com','+33 6 66 77 88 99','petitethomas99', 'False'),
(7,'Richard','Emma','emma.richard@gmail.com','+33 6 77 88 99 10','richardemma10', 'False'),
(8,'Yahiaoui','Lyes','lyes.yahiaoui@gmail.com','+33 6 19 98 78 59','yahiaouilyes59','True'),
(9,'Garnier','Alice','alice.garnier@gmail.com','+33 6 99 10 11 12','garnieralice12','False'),
(10,'Lemoine','Victor','victor.lemoine@gmail.com','+33 6 01 23 45 67','lemoinevictor67','False'),
(11,'Fournier','Chloé','chloe.fournier@gmail.com','+33 6 14 15 16','fournierchloé16','False'),
(12,'Roche','Antoine','antoine.roche@gmail.com','+33 6 17 18 19','rocheantoine19', 'False'),
(13,'Lambert','Juliette','juliette.lambert@gmail.com','+33 6 20 21 22','lambertjuliette22', 'False'),
(14,'Dumas','Julien','julien.dumas@gmail.com','+33 6 23 24 25','dumasjulien25', 'False'),
(15,'Carpentier','Claire','claire.carpentier@gmail.com','+33 6 26 27 28','carpentierclaire28','false');
(16, 'François', 'Delbot', 'francois.delbot@gmail.com', '0721346789', 'françoisdelbot', 'true'),
(17, 'HAMMA', 'Redouane', 'redouane.hamma@gmail.com', '0619987859', 'hammaredouane', 'false'),
(19, 'YAHIAOUI', 'LYES', 'lyesyahiaoui1007@gmail.com', '0619987858', 'lyesyahiaoui', 'true'),
(21, 'khoulef', 'achour', 'khoulef.achour@gmail.com', '0670399666', 'khoulefachour', 'false');


INSERT INTO gestionnaire (id_admin) VALUES 
(17);
INSERT INTO gestionnaire (id_admin) VALUES 
(19);

---Filling table sortie :
INSERT INTO sortie (id_sortie, theme, lieu_rdv, date_rdv, dparcours, effectif_max) VALUES
(1, 'Observation des oiseaux migrateurs', 'Parc National', '2024-05-01 09:00:00', 5, 20),
(2, 'Randonnée ornithologique', 'Forêt de Fontainebleau', '2024-06-15 08:30:00', 10, 15),
(3, 'Atelier de nidification', 'Jardin Botanique', '2024-04-20 14:00:00', 3, 10),
(4, 'Sortie nocturne', 'Lac de Saint-Cassien', '2024-07-10 21:00:00', 4, 12),
(5, 'Observation des rapaces', 'Colline de la Croix-Rousse', '2024-08-05 07:00:00', 6, 25),
(6, 'Excursion en bateau', 'Lac Léman', '2024-09-12 10:00:00', 8, 30),
(7, 'Séance photo des oiseaux', 'Réserve Naturelle', '2024-10-01 16:00:00', 2, 18),
(8, 'Journée de nettoyage de la plage', 'Plage de Biarritz', '2024-11-15 09:30:00', 5, 25),
(9, 'Observation des oiseaux chanteurs', 'Parc de la Tête ', '2024-12-20 08:00:00', 3, 20),
(10, 'Sortie familiale ornithologique', 'Zoo de Vincennes', '2024-05-15 10:30:00', 4, 40),
(11, 'Formation sur les espèces locales', 'Maison de la Nature', '2024-06-25 09:00:00', 2, 15),
(12, 'Atelier de construction de nichoirs', 'Centre Écologique', '2024-07-30 14:00:00', 3, 12),
(13, 'Sortie d\''observation à l\''aube', 'Réserve Ornithologique du Teich', '2024-08-20 06:30:00', 5, 20),
(14, 'Randonnée et observation des migrateurs', 'Montagne Sainte-Victoire', '2024-09-05 07:30:00', 7, 18),
(15, 'Sortie en kayak pour observer les oiseaux aquatiques', 'Rivière Dordogne', '2024-10-10 11:00:00', 6, 15);
(16, 'Randonnée sauvage', 'montagne Djurdjura en Kabylie', '2026-12-17 18:30:00', 180.0, 150),
(17, 'randonnée nanterienne', 'ufr segmi', '2026-01-10 23:59:00', 99.0, 99999);

---Filling table nichoir :
INSERT INTO nichoir (idn,date_inst,lieu_inst) VALUES
 (1,'2023-03-01' ,'Jardin de l’école'), 
 (2,'2023-04-05' ,'Parc municipal'), 
 (3,'2023-05-10' ,'Forêt de Fontainebleau'), 
 (4,'2023-06-15' ,'Jardin botanique'), 
 (5,'2023-07-20' ,'Réserve naturelle'), 
 (6,'2023-08-25' ,'Plage de Biarritz'), 
 (7,'2023-09-30' ,'Montagne Sainte-Victoire'), 
 (8,'2023-10-05' ,'Lac Léman'), 
 (9,'2023-11-10' ,'Parc de la Tête d\''Or'), 
 (10,'2023-12-15' ,'Colline de la Croix-Rousse'), 
 (11,'2024-01-20' ,'Zoo de Vincennes'), 
 (12,'2024-02-25' ,'Réserve Ornithologique du Teich'), 
 (13,'2024-03-30' ,'Rivière Dordogne'), 
 (14,'2024-04-04' ,'Lac du Der'), 
 (15,'2024-05-09' ,'Parc naturel régional');


---Filling observe_nichoir : 
INSERT INTO observe_nichoir (nbr_oeuf, type_occ, periode_nid, idn, id_adh) VALUES
(3, 'Nidification', 'Mars - Avril', 1, 1),   -- Nichoir 1 avec espèce 1
(4, 'Nidification', 'Avril - Mai', 2, 2),    -- Nichoir 2 avec espèce 2
(2, 'Nidification', 'Mai - Juin', 3, 3),     -- Nichoir 3 avec espèce 3
(5, 'Nidification', 'Juin - Juillet', 4, 4), -- Nichoir 4 avec espèce 4
(6, 'Nidification', 'Juillet - Août', 5, 5), -- Nichoir 5 avec espèce 5
(1, 'Nidification', 'Août - Septembre', 6, 6), -- Nichoir 6 avec espèce 6
(3, 'Nidification', 'Septembre - Octobre', 7, 7), -- Nichoir 7 avec espèce 7
(0, 'Non occupé', 'Aucune', 8, 8),            -- Nichoir 8 sans occupation
(2, 'Nidification', 'Octobre - Novembre', 9, 9), -- Nichoir 9 avec espèce 9
(4, 'Nidification', 'Novembre - Décembre', 10,10), -- Nichoir10 avec espèce10
(5, 'Nidification', 'Décembre - Janvier',11 ,11), -- Nichoir11 avec espèce11
(3, 'Nidification', 'Janvier - Février',12 ,12), -- Nichoir12 avec espèce12
(2, 'Non occupé', 'Aucune',13 ,13),           -- Nichoir13 sans occupation
(1, 'Nidification', 'Février - Mars',14 ,14), -- Nichoir14 avec espèce14
(4, 'Nidification', 'Mars - Avril',15 ,15);   -- Nichoir15 avec espèce15

 
---Filling table anime :
INSERT INTO anime (id_adh, id_sortie, id_animateur) VALUES
(1, 1, 1),  -- Adhérent 1 participe à la sortie 1 avec l'animateur 1
(2, 1, 2),  -- Adhérent 2 participe à la sortie 1 avec l'animateur 2
(3, 2, 1),  -- Adhérent 3 participe à la sortie 2 avec l'animateur 1
(4, 2, 3),  -- Adhérent 4 participe à la sortie 2 avec l'animateur 3
(5, 3, 2),  -- Adhérent 5 participe à la sortie 3 avec l'animateur 2
(6, 3, 4),  -- Adhérent 6 participe à la sortie 3 avec l'animateur 4
(7, 4, 1),  -- Adhérent 7 participe à la sortie 4 avec l'animateur 1
(8, 5, 3),  -- Adhérent 8 participe à la sortie 5 avec l'animateur 3
(9, 5, 2), -- Adhérent 9 participe à la sortie 5 avec l'animateur 2
(10,6 ,1), -- Adhérent10 participe à la sortie6 avec l'animateur1
(11 ,7 ,2),-- Adhérent11 participe à la sortie7 avec l'animateur2
(12 ,8 ,3),-- Adhérent12 participe à la sortie8 avec l'animateur3
(13 ,9 ,4),-- Adhérent13 participe à la sortie9 avec l'animateur4
(14 ,10 ,1),-- Adhérent14 participe à la sortie10 avec l'animateur1
(15 ,11 ,2);-- Adhérent15 participe à la sortie11 avec l'animateur2

---Filling table inscrit :
INSERT INTO inscrit (id_adh, id_sortie, date_s) VALUES
(1, 1, '2024-04-01'),  -- Adhérent 1 s'inscrit à la sortie 1
(2, 1, '2024-04-01'),  -- Adhérent 2 s'inscrit à la sortie 1
(3, 2, '2024-06-15'),  -- Adhérent 3 s'inscrit à la sortie 2
(4, 2, '2024-06-15'),  -- Adhérent 4 s'inscrit à la sortie 2
(5, 3, '2024-04-20'),  -- Adhérent 5 s'inscrit à la sortie 3
(6, 3, '2024-04-20'),  -- Adhérent 6 s'inscrit à la sortie 3
(7, 4, '2024-07-10'),  -- Adhérent 7 s'inscrit à la sortie 4
(8, 5, '2024-08-05'),  -- Adhérent 8 s'inscrit à la sortie 5
(9, 5, '2024-08-05'),   -- Adhérent 9 s'inscrit à la sortie 5
(10,6 ,'2024-09-12'),   -- Adhérent10 s'inscrit à la sortie6 
(11 ,7 ,'2024-10-01'),   -- Adhérent11 s'inscrit à la sortie7 
(12 ,8 ,'2024-11-15'),   -- Adhérent12 s'inscrit à la sortie8 
(13 ,9 ,'2024-12-20'),   -- Adhérent13 s'inscrit à la sortie9 
(14 ,10 ,'2025-01-15'),   -- Adhérent14 s'inscrit à la sortie10 
(15 ,11 ,'2025-02-20');   -- Adhérent15 s'inscrit à la sortie11 


---Filling table paye :
INSERT INTO paye (id_adh,id_status,id_cot,moy_p,date_pay) VALUES
(1,1,1,'Carte bancaire','2023-01-15'),
(2,1,2,'Espèces','2023-02-20'),
(3,2,1,'Virement bancaire','2023-03-25'),
(4,2,2,'Carte bancaire','2023-04-30'),
(5,1,1,'Espèces','2023-05-05'),
(6,1,2,'Virement bancaire','2023-06-10'),
(7,2,1,'Carte bancaire','2023-07-15'),
(8,2,2,'Espèces','2023-08-20'),
(9,1,1,'Virement bancaire','2023-09-25');

---Filling table observe :
INSERT INTO observe (id_adh,id_especes) VALUES
(1,1),
(1,2),
(2,3),
(2,4),
(3,5),
(3,6),
(4,7),
(5,8),
(5,9),
(6,10),
(7,11),
(8,12);
---Filling table regarder :
INSERT INTO regarder (idn, id_adh) VALUES
(2, 1),  -- Adhérent 1 regarde le nichoir 2
(3, 2),  -- Adhérent 2 regarde le nichoir 3
(4, 2),  -- Adhérent 2 regarde le nichoir 4
(5, 3),  -- Adhérent 3 regarde le nichoir 5
(6, 4),  -- Adhérent 4 regarde le nichoir 6
(7, 5),  -- Adhérent 5 regarde le nichoir 7
(8, 6),  -- Adhérent 6 regarde le nichoir 8
(9, 7),  -- Adhérent 7 regarde le nichoir 9
(10, 8), -- Adhérent 8 regarde le nichoir 10
(11, 9), -- Adhérent 9 regarde le nichoir 11
(12, 10),-- Adhérent 10 regarde le nichoir 12
(13, 11),-- Adhérent 11 regarde le nichoir 13
(14, 12),-- Adhérent 12 regarde le nichoir 14
(15, 13);-- Adhérent 13 regarde le nichoir 15


---Filling table specialisation :
INSERT INTO specialisation (id_adh, specialite) VALUES
(1, 'Ornithologie avancée'),
(2, 'Photographie ornithologique'),
(3, 'Éducation environnementale'),
(4, 'Conservation des espèces menacées'),
(5, 'Identification des oiseaux migrateurs'),
(6, 'Gestion des habitats naturels'),
(7, 'Biodiversité et écologie urbaine'),
(8, 'Suivi ornithologique par satellite'),
(9, 'Sensibilisation du public à l\''ornithologie'),
(10, 'Recherche sur les comportements aviaires'),
(11, 'Analyse des populations d\''oiseaux'),
(12, 'Étude de l\''habitat des oiseaux'),
(13, 'Suivi des migrations aviaires'),
(14, 'Évaluation des impacts environnementaux'),
(15, 'Protection des habitats naturels');



