
import zope.interface

from zope.publisher.interfaces.browser import IBrowserRequest

class ViewletNotFoundException(RuntimeError):
    """ Special exception for the cases we didn't found a viewlet the user asked through traversing """

class ViewletProcessingFailsException(RuntimeError):
    """ Special exception for the cases viewlet update() or render() raises exception """
        
