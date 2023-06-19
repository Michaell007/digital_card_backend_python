# ReadMe Please

Obtenir une connexion à la base de données 

    conn = mysql.connection

Créer un objet curseur 

    cursor = conn.cursor()

Exécuter une requête 

    SELECT query = "SELECT * FROM your_table" 
    cursor.execute(query)

Exécuter la requête  SELECT avec clause WHERE et paramètres 

    param1 = 'value1' 
    param2 = 'value2' 
    param3 = 'value3'  
    query = "SELECT * FROM your_table WHERE column1 = %s AND column2 = %s AND column3 = %s" 
    cursor.execute(query, (param1, param2, param3))

Récupérer les résultats de la requête 

    results = cursor.fetchall()

Vérifier si aucun résultat n'a été retourné  

    if cursor.rowcount == 0: 
        print("Aucune donnée trouvée.")

Convertir les résultats en JSON 

    json_data = jsonify(results)

Afficher les résultats  

    for row in results: 
    	print(row)
Fermer le curseur et la connexion 

    cursor.close()
