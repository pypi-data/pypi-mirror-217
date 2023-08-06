"""
Este es el modulo que oincluye la clase
de reproductor de musica
"""
    
class Player:
    """
    Esta clase crea un reproductor de musica
    """
    def play(self, song):
        """
        Reproduc la cancion que recibio como parametro
        Parameters:
            song (str): este es un strin con el path de la cancion
            
        Returns:
        int: Devuelve 1 si reproduce con exito, en
        caso contrario devuelve 0
        """
        print("reproduciendo cancion")
    def stop(self):
        print("stopping song")