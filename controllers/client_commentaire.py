#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

from controllers.client_liste_envies import client_historique_add

client_commentaire = Blueprint('client_commentaire', __name__,
                        template_folder='templates')


@client_commentaire.route('/client/article/details', methods=['GET'])
def client_article_details():
    mycursor = get_db().cursor()
    id_article =  request.args.get('id_article', None)
    id_client = session['id_user']

    ## partie 4
    # client_historique_add(id_article, id_client)

    sql = '''
    SELECT g.id_gant as id_article, g.nom_gant as nom, g.prix_gant as prix, g.image_gant as image, g.description_gant as description, 
    AVG(n.note) as moyenne_notes, COUNT(n.note) as nb_notes
    FROM gant g
    LEFT JOIN note n
    ON g.id_gant=n.id_gant
    WHERE g.id_gant = %s;
    '''
    mycursor.execute(sql, id_article)
    article = mycursor.fetchone()
    commandes_articles=[]
    nb_commentaires=[]
    if article is None:
        abort(404, "pb id gant")
    
    sql = '''SELECT c.commentaire, u.nom, c.id_utilisateur, c.id_gant AS id_article, c.date_publication, c.valider
    FROM commentaire c 
    INNER JOIN utilisateur u 
    ON c.id_utilisateur=u.id_utilisateur 
    WHERE id_gant=%s
    ORDER BY c.date_publication DESC;'''
    mycursor.execute(sql, ( id_article))
    commentaires = mycursor.fetchall()
    sql = '''SELECT COUNT(id_utilisateur) AS nb_commandes_article
    FROM commande co
    INNER JOIN ligne_commande lc
    ON co.id_commande=lc.id_commande
    INNER JOIN declinaison de
    ON lc.id_declinaison=de.id_declinaison
    INNER JOIN gant ga
    ON de.id_gant=ga.id_gant
    WHERE co.id_utilisateur=%s AND ga.id_gant=%s;
    '''
    mycursor.execute(sql, (id_client, id_article))
    commandes_articles = mycursor.fetchone()
    sql = '''
    SELECT note
    FROM note
    WHERE id_utilisateur=%s AND id_gant=%s;
    '''
    mycursor.execute(sql, (id_client, id_article))
    note = mycursor.fetchone()
    if note:
        note=float(note['note'])
    print("note : ", note,)
    sql = '''
    SELECT 
    (SELECT COUNT(*) FROM commentaire WHERE id_utilisateur = %s AND id_gant = %s) AS nb_commentaires_utilisateur,
    (SELECT COUNT(*) FROM commentaire WHERE id_gant = %s) AS nb_commentaires_total;
    '''
    mycursor.execute(sql, (id_client, id_article, id_article))
    nb_commentaires = mycursor.fetchone()
    
    return render_template('client/article_info/article_details.html'
                           , article=article
                           , commentaires=commentaires
                           , commandes_articles=commandes_articles
                           , note=note
                            , nb_commentaires=nb_commentaires
                           )

@client_commentaire.route('/client/commentaire/add', methods=['POST'])
def client_comment_add():
    mycursor = get_db().cursor()
    commentaire = request.form.get('commentaire', None)
    id_client = session['id_user']
    id_article = request.form.get('id_article', None)
    if commentaire == '':
        flash(u'Commentaire non pris en compte', 'alert-warning')
        return redirect('/client/article/details?id_article='+id_article)
    if commentaire != None and len(commentaire)>0 and len(commentaire) <3 :
        flash(u'Commentaire avec plus de 2 caractères','alert-warning')              # 
        return redirect('/client/article/details?id_article='+id_article)

    tuple_insert = (id_article, id_client, commentaire)
    print(tuple_insert)
    sql = '''   INSERT INTO commentaire VALUES
    (%s, %s, NOW(), %s, FALSE)'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)


@client_commentaire.route('/client/commentaire/delete', methods=['POST'])
def client_comment_detete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article', None)
    date_publication = request.form.get('date_publication', None)
    sql = '''
    DELETE FROM commentaire 
    WHERE id_utilisateur=%s 
    AND id_gant=%s 
    AND date_publication LIKE %s
    '''
    tuple_delete=(id_client,id_article,date_publication)
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)

@client_commentaire.route('/client/note/add', methods=['POST'])
def client_note_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    note = request.form.get('note', None)
    id_article = request.form.get('id_article', None)
    tuple_insert = (note, id_client, id_article)
    print(tuple_insert)
    sql = '''
    INSERT INTO note (note, id_utilisateur, id_gant)
    VALUES (%s, %s, %s);
    '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)

@client_commentaire.route('/client/note/edit', methods=['POST'])
def client_note_edit():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    note = request.form.get('note', None)
    id_article = request.form.get('id_article', None)
    tuple_update = (note, id_client, id_article)
    print(tuple_update)
    sql = '''
    UPDATE note
    SET note=%s
    WHERE id_utilisateur=%s
    AND id_gant=%s
    '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)

@client_commentaire.route('/client/note/delete', methods=['POST'])
def client_note_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article', None)
    tuple_delete = (id_client, id_article)
    print(tuple_delete)
    sql = '''
    DELETE FROM note
    WHERE id_utilisateur=%s
    AND id_gant=%s
    '''
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)
