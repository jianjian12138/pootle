from translate.storage import statsdb

STATS_DB_FILE = None

def getmodtime(filename):
  try:
    mtime, _size = statsdb.get_mod_info(filename)
    return mtime
  except:
    return None

def memoize(f):
  def memoized_f(self, *args, **kwargs):
    f_name = f.__name__
    table = self._memoize_table
    if f_name not in table:
      table[f_name] = f(self, *args, **kwargs)
    return table[f_name]
  return memoized_f

class pootlestatistics:
  """this represents the statistics known about a file"""
  def __init__(self, basefile):
    """constructs statistic object for the given file"""
    # TODO: try and remove circular references between basefile and this class
    self.basefile = basefile
    self.statscache = statsdb.StatsCache(STATS_DB_FILE)
    self._memoize_table = {}

  @memoize
  def getquickstats(self):
    """returns the quick statistics (totals only)"""
    try:
      return self.statscache.filetotals(self.basefile.filename) or statsdb.emptyfiletotals()
    except:
      return statsdb.emptyfiletotals()

  @memoize
  def getstats(self, checker=None):
    """reads the stats if neccessary or returns them from the cache"""
    if checker == None:
      checker = self.basefile.checker
    try:
      return self.statscache.filestats(self.basefile.filename, checker)
    except:
      return statsdb.emptyfilestats()

  @memoize
  def getunitstats(self):
    try:
      return self.statscache.unitstats(self.basefile.filename)
    except:
      return statsdb.emptyunitstats()

  def reclassifyunit(self, item):
    """Reclassifies all the information in the database and self._stats about
    the given unit"""
    unit = self.basefile.getitem(item)
    self.statscache.recacheunit(self.basefile.filename, self.basefile.checker, unit)
    self._memoize_table = {}

  @memoize
  def getitemslen(self):
    """gets the number of items in the file"""
    return self.getquickstats()["total"]
