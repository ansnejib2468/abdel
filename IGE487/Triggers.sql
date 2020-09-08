-- Trigger pour le choix d'une date de réservation de terrain 
CREATE TRIGGER "dispo_terrains"
BEFORE INSERT OR UPDATE
ON Reservation
FOR EACH ROW EXECUTE PROCEDURE TerrainsComplets();

-- trigger pour réserver un terrain à une date 
CREATE TRIGGER "PossibleReservation_terrains"
BEFORE INSERT OR UPDATE
ON Reservation
FOR EACH ROW EXECUTE PROCEDURE TerrainDispo();

-- trigger pour réserver un vestiaire à une date 
CREATE TRIGGER "PossibleReservation_terrains"
BEFORE INSERT OR UPDATE
ON Reservation
FOR EACH ROW EXECUTE PROCEDURE Equipement_Dispo();

-- trigger pour réserver un equipement à une date 
CREATE TRIGGER "PossibleReservation_terrains"
BEFORE INSERT OR UPDATE
ON Reservation
FOR EACH ROW EXECUTE PROCEDURE Vestiaire_Dispo();

-- trigger pour mettre a jour l'état d'un terrain 
CREATE TRIGGER "Terrain_Réservé"
AFTER INSERT OR UPDATE
ON Reservation
FOR EACH ROW EXECUTE PROCEDURE Etat_Terrain();

