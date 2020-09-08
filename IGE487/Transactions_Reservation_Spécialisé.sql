/*Dans un contexte de centre sportif Spécialisé*/ 
/* Ajouter une réservation pour un client existant à partir de son nom et son téléphone*/
/*Pour se faire on doit avoir une fonction qui trouve le id du client à partir de son tel et son nom  */
/* Une autre fonction qui vérifie s'il y a des terrains disponibles*/
/*On attribue au client le premier terrain disponible trouvé*/
/* On prend en compte le fait que les états de tous les terrains sont mis à jour régulièrement grace à la fonction Etat_Terrain()*/
/* Nous avons un Trigger qui s'occupe de déterminer si à une date précise, il est possible de réserver un terrain*/

CREATE FUNCTION find_client(nomC text_court_domaine, telC CHAR(10))
RETURNS idclient_domaine AS
$$
BEGIN
IF 1=(
WITH Client_valide AS(SELECT idClient
FROM Client
WHERE nom =nomC AND tel = telC
)
SELECT COUNT(*)
FROM Client_valide
)
THEN
RETURN Client_valide.idClient;
END IF;
RAISE EXCEPTION 'Ce client n esxiste pas';
RETURN NULL; 
END;
$$
LANGUAGE plpgsql;



CREATE FUNCTION find_TerrainDispo()
IF 0=(                         select count(distinct idTerrain)
							   from Terrain 
							   Where Disponible = true
							   )
THEN
RAISE EXCEPTION 'Aucun terrain Disponible';
RETURN NULL; 
ELSE 
RETURNS idTerrain_domaine AS ( select idTerrain
							   from Terrain 
							   Where Disponible = true 
							   order by idTerrain
							   fetch first row only; )
END IF;
END;
$$
LANGUAGE plpgsql;


START TRANSACTION READ WRITE;
SET CONSTRAINTS ALL DEFERRED;
INSERT INTO Réservation(idClient,idTerrain,idPatient,dateDebut,dateFin,HeureDebut,HeureFin,TypeReservation,description) VALUES
(find_client('Pierre','8195775069'),find_TerrainDispo(),'2018-01-06','2018-01-08','12:00','14:00','Amical', 'reservation pour un groupe d amis jouant au soccer');
SET CONSTRAINTS ALL IMMEDIATE;
COMMIT;
