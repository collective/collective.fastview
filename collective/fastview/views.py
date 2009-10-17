"""


"""

from Acquisition import aq_inner
import zope.interface

from plone.app.customerize import registration

from Products.Five.browser import BrowserView

from zope.traversing.interfaces import ITraverser, ITraversable
from zope.publisher.interfaces import IPublishTraverse, NotFound
from zope.publisher.interfaces.browser import IBrowserRequest

from collective.fastview.interfaces import IGlobalDefineFreeRender

class HasGlobalDefines(BrowserView):
    """ View that exposes whether global defines should be included in main template or not.

    """

    def __call__(self):
        """ @return: True of False """
        fast_mode = IGlobalDefineFreeRender.providedBy(self.request)
        print "Got fast mode:" + str(fast_mode)
        return not fast_mode

    def render(self):
        """
        """
        raise RuntimeError("This view is supposed to be called as utility")



class Viewlets(BrowserView):
    """ Viewlet renderer helper.

    Expose viewlets to templates by names.
    Grok maps this view to every context as "@@viewlets" traversing point.

    Example how to render plone.logo viewlet in arbitary template code point::

        <div tal:content="context/@@viewlets/plone.logo" />

    """
    zope.interface.implements(ITraversable)

    def getViewletByName(self, name):
        """
        @return: Viewlet registration object
        """
        views = registration.getViews(IBrowserRequest)
        for v in views:
            if v.name == name: return v
        return None


    def renderViewletByName(self, name):
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
        viewlet = factory(context, request, self, None).__of__(context)

        # Perform viewlet computations
        viewlet.update()
        return viewlet.render()

    def traverse(self, name, furthet_path):
        """
        Allow travering intoviewlets by viewlet name.

        @return: Viewlet HTML output

        @raise: RuntimeError if viewlet is not found
        """
        html = self.renderViewletByName(name)
        if html == None:
            raise NotFound("No viewlet registration by name %s" % name)

        return html

    def publishTraverse(self, request, name):
        """
        Allow travering intoviewlets by viewlet name.

        @return: Viewlet HTML output

        @raise: RuntimeError if viewlet is not found
        """
        html = self.renderViewletByName(name)
        if html == None:
            raise NotFound("No viewlet registration by name %s" % name)

        return html