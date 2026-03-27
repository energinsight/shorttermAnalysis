import sys
from pathlib import Path

# Add parent directory to path so we can import utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from dataframework.entsoe import EntsoeSpotPrice
from dataframework.jaoCore import Jaocore_shadowprices
from utils.plotting import shadowPlot
import pandas as pd

from utils.plotting import shadowPlot



start = pd.Timestamp('2026-03-27 0:00:00', tz='Europe/Brussels')   # 
end = pd.Timestamp('2026-03-27 23:59:00', tz='Europe/Brussels')

shadowProbj = Jaocore_shadowprices(start, end)
entsopr = EntsoeSpotPrice(start, end)

activeConst = shadowProbj.load_data()
activeConst['fuafbyfmax'] = 100 * activeConst['fuaf'] / activeConst['fmax']
y = entsopr.load_data('DE_LU')



shadowPlot(activeConst, 'shadowPrice')
shadowPlot(activeConst, 'ram')
shadowPlot(activeConst, 'fuaf')
shadowPlot(activeConst, 'iva')
shadowPlot(activeConst, 'fuafbyfmax')
