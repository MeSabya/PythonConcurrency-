```python
import time
import threading

class RequestCounters(object):
	# Every window time is broken down to 60 parts
	# 100 req/min translates to requests = 100 and windowTimeInSec = 60
	def __init__(self, requests, windowTimeInSec, bucketSize=10):
		self.counts = {}
		self.totalCounts = 0
		self.requests = requests
		self.windowTimeInSec = windowTimeInSec
		self.bucketSize = bucketSize
		self.lock = threading.Lock()

	# Gets the bucket for the timestamp
	def getBucket(self, timestamp):
		factor = self.windowTimeInSec / self.bucketSize
		return (timestamp // factor) * factor

	# Gets the bucket list corresponding to the current time window
	def _getOldestvalidBucket(self, currentTimestamp):
		return self.getBucket(currentTimestamp - self.windowTimeInSec)

	# Remove all the older buckets that are not relevant anymore
	def evictOlderBuckets(self, currentTimestamp):
		oldestValidBucket = self._getOldestvalidBucket(currentTimestamp)
		bucketsToBeDeleted = filter(
			lambda bucket: bucket < oldestValidBucket, self.counts.keys())
		for bucket in bucketsToBeDeleted:
			bucketCount = self.counts[bucket]
			self.totalCounts -= bucketCount
			del self.counts[bucket]

class SlidingWindowCounterRateLimiter(object):
	def __init__(self):
		self.lock = threading.Lock()
		self.ratelimiterMap = {}

	# Default of 100 req/minute
	# Add a new user with a request rate
	# If a request from un-registered user comes, we throw an Exception
	def addUser(self, userId, requests=100, windowTimeInSec=60):
		with self.lock:
			if userId in self.ratelimiterMap:
				raise Exception("User already present")
			self.ratelimiterMap[userId] = RequestCounters(requests, windowTimeInSec)

	def removeUser(self, userId):
		with self.lock:
			if userId in self.ratelimiterMap:
				del self.ratelimiterMap[userId]

	@classmethod
	def getCurrentTimestampInSec(cls):
		return int(round(time.time()))

	def shouldAllowServiceCall(self, userId):
		with self.lock:
			if userId not in self.ratelimiterMap:
				raise Exception("User is not present")
		userTimestamps = self.ratelimiterMap[userId]
		with userTimestamps.lock:
			currentTimestamp = self.getCurrentTimestampInSec()
			# remove all the existing older timestamps
			userTimestamps.evictOlderBuckets(currentTimestamp)
			currentBucket = userTimestamps.getBucket(currentTimestamp)
			userTimestamps.counts[currentBucket] = userTimestamps.counts.
				get(currentBucket, 0) + 1
			userTimestamps.totalCounts += 1
			if userTimestamps.totalCounts > userTimestamps.requests:
				return False
			return True
      
  ```
