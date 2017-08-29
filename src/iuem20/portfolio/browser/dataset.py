# -*- coding: utf-8 -*-

from os.path import abspath
from os.path import dirname
from os.path import join
from plone import api
from plone.app.textfield.value import RichTextValue
from plone.namedfile import NamedBlobImage
from zope.publisher.browser import BrowserView

import logging


PREFIX = abspath(dirname(__file__))
logger = logging.getLogger('iuem20.portfolio: CREATEDATASET')


def input_image_path(f):
    return join(PREFIX, '../tests/images/', f)


lorem = """
Vivamus dictum, nunc a tincidunt semper, lectus justo maximus neque,
et pulvinar ipsum dolor at nisl. Maecenas porttitor dolor nec ante cursus
viverra. Maecenas massa nunc, semper vitae pulvinar at, semper
at metus. Cras a fermentum diam. Sed a lobortis
risus, efficitur tincidunt lorem.
"""

bio_fr_text = """
<h4>Savoir-faire opérationnels</h4>
<ul>
<li>Utiliser les méthodes de prévention et
de gestion des risques<br/></li>
</ul>
<h4>Lieu d'exercice</h4>
<ul>
<li>L’activité s’exerce généralement au sein d'un service informatique<br/>
</li>
</ul>
<h3>Dipl&ocirc;me exig&eacute;</h3>
<ul>
<li>Doctorat, diplôme d’ingénieur<br/></li>
</ul>
<h3>Formations et expérience professionnelle souhaitables</h3>
<ul><li>Filière informatique</li></ul>
"""

bio_alt1_text = """
<h2>ALT 1 The RichTextValue<a class="headerlink" href="#the-richtextvalue"
title="Permalink to this headline">¶</a></h2>
<p>The <code class="docutils literal"><span class="pre">RichText</span>
</code> field does not store a string. Instead, it stores a
<code class="docutils literal"><span class="pre">RichTextValue</span>
</code> object. This is an immutable object that has the
following properties:</p>
<dl class="docutils">
<dt><code class="docutils literal"><span class="pre">raw</span></code></dt>
<dd>a unicode string with the original input markup;</dd>
<dt><code class="docutils literal"><span class="pre">mimeType</span></code>
</dt>
<dd>the MIME type of the original markup, e.g.
<code class="docutils literal"><span class="pre">text/html</span></code> or
<code class="docutils literal"><span class="pre">text/structured</span>
</code>;</dd>
<dt><code class="docutils literal"><span class="pre">encoding</span></code>
</dt>
<dd>the default character encoding used when transforming the input markup.
Most likely, this will be UTF-8;</dd>
<dt><code class="docutils literal"><span class="pre">raw_encoded</span>
</code></dt>
<dd>the raw input encoded in the given encoding;</dd>
<dt><code class="docutils literal"><span class="pre">outputMimeType</span>
</code></dt>
<dd>the MIME type of the default output, taken from the field at the time of
instantiation;</dd>
<dt><code class="docutils literal"><span class="pre">output</span></code></dt>
<dd>a unicode object representing the transformed output. If possible, this
is cached persistently until the <code class="docutils literal">
<span class="pre">RichTextValue</span></code> is replaced with a
new one (as happens when an edit form is saved, for example).</dd>
</dl>
"""
bio_alt2_text = """
<h2>ALT 2 The RichTextValue<a class="headerlink" href="#the-richtextvalue"
title="Permalink to this headline">¶</a></h2>
<p>The <code class="docutils literal"><span class="pre">RichText</span>
</code> field does not store a string. Instead, it stores a
<code class="docutils literal"><span class="pre">RichTextValue</span>
</code> object. This is an immutable object that has the
following properties:</p>
<dl class="docutils">
<dt><code class="docutils literal"><span class="pre">raw</span></code></dt>
<dd>a unicode string with the original input markup;</dd>
<dt><code class="docutils literal"><span class="pre">mimeType</span></code>
</dt>
<dd>the MIME type of the original markup, e.g.
<code class="docutils literal"><span class="pre">text/html</span></code> or
<code class="docutils literal"><span class="pre">text/structured</span>
</code>;</dd>
<dt><code class="docutils literal"><span class="pre">encoding</span></code>
</dt>
<dd>the default character encoding used when transforming the input markup.
Most likely, this will be UTF-8;</dd>
<dt><code class="docutils literal"><span class="pre">raw_encoded</span>
</code></dt>
<dd>the raw input encoded in the given encoding;</dd>
<dt><code class="docutils literal"><span class="pre">outputMimeType</span>
</code></dt>
<dd>the MIME type of the default output, taken from the field at the time of
instantiation;</dd>
<dt><code class="docutils literal"><span class="pre">output</span></code></dt>
<dd>a unicode object representing the transformed output. If possible, this
is cached persistently until the <code class="docutils literal">
<span class="pre">RichTextValue</span></code> is replaced with a
new one (as happens when an edit form is saved, for example).</dd>
</dl>
"""

bio_fr = RichTextValue(bio_fr_text, 'text/plain', 'text/html')

bio_alt1 = RichTextValue(bio_alt1_text, 'text/plain', 'text/html')
bio_alt2 = RichTextValue(bio_alt2_text, 'text/plain', 'text/html')


po = {}
po['title'] = u'Mon Portfolio'
po['description'] = u'Et là, on a de la chance de revenir entiers !'
po['presentation'] = bio_fr
po['image'] = u'1800-IMGA0215.JPG'
po['img_author'] = u'AAUUtthhZZZ'
po['thumbnail'] = u'200-IMGA0537.JPG'
po['display_one'] = True
po['presentation_one'] = bio_alt1
po['display_two'] = True
po['presentation_two'] = bio_alt1


class createDataSet(BrowserView):

    def __call__(self):
        portal = api.portal.get()
        self.deletePortfolio()
        self.createPortfolio()
        url = portal.absolute_url() + '/folder_contents'
        self.request.response.redirect(url)

    def deletePortfolio(self):
        portal = api.portal.get()
        try:
            title = u'mon-portfolio'
            api.content.delete(obj=portal[title])
        except Exception:
            pass

    def _loadImage(self, objField, image):
        imgPath = image.split('/')
        if len(imgPath) > 1:
            title = imgPath[len(imgPath) - 1]
        else:
            title = image
        path = input_image_path(image)
        fd = open(path, 'r')
        objField.data = fd.read()
        fd.close()
        objField.filename = title

    def createPortfolio(self):
        portal = api.portal.get()
        portfolio = api.content.create(
            type='iuem20.portfolio',
            title=po['title'],
            description=po['description'],
            presentationr=po['presentation'],
            display_one=po['display_one'],
            presentation_one=po[
             'presentation_one'],
            display_two=po['display_two'],
            presentation_two=po[
             'presentation_two'],
            image=NamedBlobImage(),
            img_author=po['img_author'],
            thumbnail=NamedBlobImage(),
            container=portal)
        portfolio.presentation = po['presentation']
        self._loadImage(portfolio.image, po['image'])
        # image
        # Thumbnail
        self._loadImage(portfolio.thumbnail, po['thumbnail'])
        portfolio.reindexObject()
        logger.info(portfolio.title + ' Created')
        imgs = [u'1800-IMGA0108.JPG', u'900-IMGA0052.JPG',
                u'1800-IMGA0214.JPG', u'1800-IMGA0215.JPG',
                u'200-IMGA0465.JPG', u'200-IMGA0487.JPG',
                u'1800-IMGA0212.JPG', u'200-IMGA0536.JPG',
                u'900-IMGA0042.JPG', u'900-IMGA0045.JPG',
                u'200-IMGA0537.JPG', u'900-IMGA0054.JPG']
        self._loadImagesInFolder(portfolio, imgs)
        authors = api.content.create(
            type='Folder',
            title='authors',
            container=portfolio)
        imgs = [u'200-IMGA0108.JPG', u'200-IMGA0212.JPG',
                u'200-IMGA0214.JPG']
        self._loadImagesInFolder(authors, imgs)

    def _loadImagesInFolder(self, folderish, images):
        for img in images:
            imgPath = img.split('/')
            if len(imgPath) > 1:
                title = imgPath[len(imgPath) - 1]
            else:
                title = img
            image = api.content.create(type='Image',
                                       title=title,
                                       image=NamedBlobImage(),
                                       description=lorem,
                                       container=folderish)
            self._loadImage(image.image, img)
            image.reindexObject()
            api.content.transition(obj=image, transition='publish')
            image.reindexObject()
