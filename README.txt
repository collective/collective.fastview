.. contents ::

Introduction
-------------

collective.fastview provides framework level helper code for Plone view and template management.

Installation
------------

Add collective.fastview to buildout eggs list::

        eggs = 
                ...
                collective.fastview

Render viewlets without viewlet manager
---------------------------------------

You can directly put in viewlet call to any page template code 
using a viewlet traverser. collective.fastview registers
a view with name @@viewlets which you can use to traverse 
to render any viewlet code::

        <div id="header">
            <div tal:replace="structure context/@@viewlets/plone.logo" />
        </div>

Fix Grok 1.0 template inheritance
---------------------------------

This fixes grok 1.0 problem that view and viewlets template are not inheritable between packages.
E.g. if you subclass a view you need to manually copy over the view template also.
    
We hope to get rid of this with Plone 4 / fixed grok.
    
See:
    
* https://bugs.launchpad.net/grok/+bug/255005

Example::

        from collective.fastview.utilities import fix_grok_template_inheritance
        from gomobiletheme.basic import viewlets as base
        from gomobiletheme.basic.viewlets import MainViewletManager
        from plonecommunity.app.interfaces import IThemeLayer
        
        # Viewlets are on all content by default.
        grok.context(Interface)
        
        # Use templates directory to search for templates.
        grok.templatedir("templates")
        
        # Viewlets are active only when gomobiletheme.basic theme layer is activated
        grok.layer(IThemeLayer)
        
        grok.viewletmanager(MainViewletManager)
        
        class Head(base.Head):
            """
            Override <head> generation so that we use CSS files 
            and static resources specific to this skin.
            """
            
            def resource_url(self):
                """ Get static resource URL.
                
                See gomobiletheme.basic.viewlets.Head for more information.
                """
                return self.portal_url + "/" + "++resource++plonecommunity.app"
            
        # Fix for grok 1.0 template inheritance
        # https://bugs.launchpad.net/grok/+bug/255005
        fix_grok_template_inheritance(Head, base.Head)


Author
------

`mFabrik Research Oy <mailto:info@mfabrik.com>`_ - Python and Plone professionals for hire.

* `mFabrik business group web site <http://mfabrik.com>`_ 

* `mFabrik business group mobile site <http://mfabrik.mobi>`_ 

* `Blog <http://blog.mfabrik.com>`_

* `More about Plone <http://mfabrik.com/technology/technologies/content-management-cms/plone>`_ 

       
      