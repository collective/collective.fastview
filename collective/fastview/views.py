"""


"""

from Acquisition import aq_inner
import zope.interface

from plone.app.customerize import registration

from Products.Five.browser import BrowserView

from zope.traversing.interfaces import ITraverser, ITraversable
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.viewlet.interfaces import IViewlet
from zExceptions import NotFound

from collective.fastview.interfaces import IGlobalDefineFreeRender

class HasGlobalDefines(BrowserView):
    """ View that exposes whether global defines should be included in main template or not.

    """

    def __call__(self):
        """ @return: True of False """
        fast_mode = IGlobalDefineFreeRender.providedBy(self.request)
        return not fast_mode

    def render(self):
        """
        """
        raise RuntimeError("This view is supposed to be called as utility")



class Viewlets(BrowserView):
    """ Expose arbitary viewlets to traversing by name.

    Exposes viewlets to templates by names.

    Example how to render plone.logo viewlet in arbitary template code point::

        <div tal:content="context/@@viewlets/plone.logo" />

    """
    zope.interface.implements(ITraversable)


    def matchLayers(self, has_layers, wanted_layers):
        """ Check that viewlet is registered for an layer which is active

        (<InterfaceClass zope.interface.Interface>, <InterfaceClass gomobiletheme.basic.interfaces.IThemeLayer>, <InterfaceClass zope.publisher.interfaces.browser.IBrowserView>, <implementedBy gomobiletheme.basic.viewlets.MainViewletManager>)

        (<InterfaceClass zope.interface.Interface>, <InterfaceClass gomobiletheme.twinapex.interfaces.IThemeLayer>, <InterfaceClass zope.publisher.interfaces.browser.IBrowserView>, <implementedBy gomobiletheme.basic.viewlets.MainViewletManager>)
        """

        # TODO: Hack - no clue how to do this properly


    def getViewletByName(self, name):
        """ Viewlets allow through-the-web customizations.

        Through-the-web customization magic is managed by five.customerize.
        We need to think of this when looking up viewlets.

        @return: Viewlet registration object
        """
        views = registration.getViews(IBrowserRequest)

        found = None

        from plone.browserlayer.utils import registered_layers
        wanted_layers = registered_layers()

        # List of all viewlet registration with the name
        # Note: several registrations possible due to layers
        possible = []

        for v in views:

            if v.provided == IViewlet:
                # Note that we might have conflicting BrowserView with the same name,
                # thus we need to check for provided
                if v.name == name:
                    possible.append(v)

        # Try match viewlets against active layers
        # Start from the browserlayer with highest priority


        # <InterfaceClass webcouturier.dropdownmenu.browser.interfaces.IDropdownSpecific>, <InterfaceClass Products.LinguaPlone.interfaces.ILinguaPloneProductLayer>, <InterfaceClass plonetheme.twinapex.browser.interfaces.IThemeSpecific>, <InterfaceClass quintagroup.seoptimizer.browser.interfaces.IPloneSEOLayer>, <InterfaceClass gomobile.mobile.interfaces.IMobileLayer>, <InterfaceClass gomobiletheme.basic.interfaces.IThemeLayer>, <InterfaceClass gomobiletheme.twinapex.interfaces.IThemeLayer>]

        wanted_layers = wanted_layers[:]
        wanted_layers.reverse()

        for layer in wanted_layers:

            for viewlet_registration in possible:

                # (<InterfaceClass zope.interface.Interface>, <InterfaceClass gomobiletheme.basic.interfaces.IThemeLayer>, <InterfaceClass zope.publisher.interfaces.browser.IBrowserView>, <implementedBy gomobiletheme.basic.viewlets.MainViewletManager>)
                theme_layer = viewlet_registration.required[1]
                if theme_layer == layer:
                    return viewlet_registration

        return None

    def getActiveLayer(self):
        """
        Get active theme layer for getting viewlets for the active theme.

        @return: Theme layer instance
        """
        portal_skins = getToolByName(self.context, "portal_skins")
        active_skin_name = portal_skins.get

    def setupViewletByName(self, name):
        """ Constructs a viewlet instance by its name.

        Viewlet update() and render() method are not called.

        @return: Viewlet instance of None if viewlet with name does not exist
        """
        context = aq_inner(self.context)
        request = self.request

        # Perform viewlet regisration look-up
        # from adapters registry
        reg = self.getViewletByName(name)
        if reg == None:
            return None

        # factory method is responsible for creating the viewlet instance
        factory = reg.factory

        # Create viewlet and put it to the acquisition chain
        # Viewlet need initialization parameters: context, request, view
        try:
            viewlet = factory(context, request, self, None).__of__(context)
        except TypeError:
            # Bad constructor call parameters
            raise RuntimeError("Unable to initialize viewlet %s. Factory method %s call failed." % (name, str(factory)))

        return viewlet

    def traverse(self, name, further_path):
        """
        Allow travering intoviewlets by viewlet name.

        @return: Viewlet HTML output

        @raise: RuntimeError if viewlet is not found
        """

        viewlet = self.setupViewletByName(name)
        if viewlet is None:
            raise NotFound("Viewlet does not exist by name %s for theme layer %s" % name)

        viewlet.update()
        return viewlet.render()

