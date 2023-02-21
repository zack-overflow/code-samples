print("Hi Stephen! I ended up implementing the data structures from scratch and doing some testing on the given inputs like you recommend. Everything runs smoothly to generate the suggested outputs and I am happy I chose to do this from scratch since I learned a ton. Hope I get the chance to talk over the solution with you and walk through the running time/efficiency and logic of my approach.")
print()
print()
#
# Your previous Go content is preserved below:
# 
# package cache
# 
# import (
#   "time"
# )
# 
# /*
# You can use any language.
# 
# Your task is to implement a PriorityExpiryCache cache with a max capacity.  Specifically please fill out the data structures on the PriorityExpiryCache object and implement the entry eviction method.
# 
# It should support these operations:
#   Get: Get the value of the key if the key exists in the cache and is not expired.
#   Set: Update or insert the value of the key with a priority value and expiretime.
#     Set should never ever allow more items than maxItems to be in the cache.
#     When evicting we need to evict the lowest priority item(s) which are least recently used.
# 
# Example:
# p5 => priority 5
# e10 => expires at 10 seconds since epoch
# 
# c = NewCache(5)
# c.Set("A", value=1, priority=5,  expireTime=100)
# c.Set("B", value=2, priority=15, expireTime=3)
# c.Set("C", value=3, priority=5,  expireTime=10)
# c.Set("D", value=4, priority=1,  expireTime=15)
# c.Set("E", value=5, priority=5,  expireTime=150)
# c.Get("C")
# 
# 
# // Current time = 0
# c.SetMaxItems(5)
# c.Keys() = ["A", "B", "C", "D", "E"]
# // space for 5 keys, all 5 items are included
# 
# time.Sleep(5)
# 
# // Current time = 5
# c.SetMaxItems(4)
# c.Keys() = ["A", "C", "D", "E"]
# // "B" is removed because it is expired.  e3 < e5
# 
# c.SetMaxItems(3)
# c.Keys() = ["A", "C", "E"]
# // "D" is removed because it the lowest priority
# // D's expire time is irrelevant.
# 
# c.SetMaxItems(2)
# c.Keys() = ["C", "E"]
# // "A" is removed because it is least recently used."
# // A's expire time is irrelevant.
# 
# c.SetMaxItems(1)
# c.Keys() = ["C"]
# // "E" is removed because C is more recently used (due to the Get("C") event).
# 
# */
# 
# type PriorityExpiryCache struct {
#   maxItems int
#   // TODO(interviewee): implement this
# }
# 
# func NewCache(maxItems int) *PriorityExpiryCache {
#   return &PriorityExpiryCache{
#     maxItems: maxItems,
#   }
# }
# 
# func (c *PriorityExpiryCache) Get(key string) interface{} {
#   // ... the interviewee does not need to implement this.
# 
#   return nil
# }
# 
# func (c *PriorityExpiryCache) Set(key string, value interface{}, priority int, expire time.Time) {
#   // ... the interviewee does not need to implement this.
# 
#   c.evictItems()
# }
# 
# func (c *PriorityExpiryCache) SetMaxItems(maxItems int) {
#   c.maxItems = maxItems
# 
#   c.evictItems()
# }
# 
# // evictItems will evict items from the cache to make room for new ones.
# func (c *PriorityExpiryCache) evictItems() {
#   // TODO(interviewee): implement this
# }

        
class MinHeap:
    def __init__(self):
        self.heap = []
        self.size = 0
        self.priority_map = {}
    
    def shift_up(self, i):
        predecessor = i // 2
        while predecessor >= 0:
            if self.heap[i][0] < self.heap[predecessor][0]:
                self.heap[i], self.heap[predecessor] =  self.heap[predecessor], self.heap[i]
                i = predecessor
                predecessor = i // 2
            else:
                break    # heap properties satisfied
        
    def shift_down(self, i):
        if self.size == 1:
            return
        while 2 * i < self.size:
            print(self.heap)
            # print("in loop")
            left_child = 2 * i
            right_child = 2 * i + 1
            if right_child < self.size:
                if self.heap[i][0] < self.heap[left_child][0] and self.heap[i][0] < self.heap[right_child][0]:
                    break    # heap properties satisfied
                else:
                    if self.heap[left_child][0] < self.heap[right_child][0]:
                        self.heap[left_child], self.heap[i] = self.heap[i], self.heap[left_child]
                        i = left_child
                    else:
                        self.heap[right_child], self.heap[i] = self.heap[i], self.heap[right_child]
                        i = right_child
            else:
                if self.heap[i][0] < self.heap[left_child][0]:
                    break    # heap properties satisfied
                else:
                    self.heap[left_child], self.heap[i] = self.heap[i], self.heap[left_child]
                    i = left_child
        
    
    def insert(self, item, flag):
        if flag == "expire heap":
            self.heap.append((item[3], item))
            self.size += 1
            self.shift_up(self.size-1)    # shift up the new node
        
        else:    # i.e. flag is priority heap
            priority = item[2]
            if priority in self.priority_map:
                self.priority_map[priority].add_node(item)
            else:
                LL = CustomLinkedList()
                LL.add_node(item)
                self.priority_map[priority] = LL 
                self.heap.append((priority, LL))
                self.size += 1
                self.shift_up(self.size-1)    # shift up the new node
    
    def find(self, val):
        i = 0
        while i < self.size:
            if self.heap[i][0] == val:
                return i
            i += 1
            
        return -1    # this should not occur, means node is not found
        
    def remove(self, val, flag):
        to_remove_index = self.find(val)
        
        # we need a flag because in one case we need to remove an item from the heap directly
        # and in the other case we need to remove it from a LL stored in the heap
        if flag == "expire heap":
            self.heap[to_remove_index], self.heap[self.size-1] = self.heap[self.size-1], self.heap[to_remove_index]
            removed = self.heap.pop()
            removed_item = removed[1]
            self.size -= 1
            
        else:
            # i.e. flag is priority heap
            LL = self.heap[to_remove_index][1]
            removed_item = LL.remove_least_recently_used(self)
            
        
        return removed_item
        
    def remove_list(self, priority):
        # shift up or down
        to_remove_index = self.find(priority)
        if to_remove_index < self.size - 1:
            self.heap[to_remove_index], self.heap[self.size-1] = self.heap[self.size-1], self.heap[to_remove_index]
            removed_item = self.heap.pop()
            self.size -= 1
        
            # now heapify again
            i = to_remove_index
            predecessor = i // 2

            if i == 0 or self.heap[predecessor][0] < self.heap[to_remove_index][0]:
                self.shift_down(i)
            else:
                self.shift_up(i)
        else:
            removed_item = self.heap.pop()
            self.size -= 1
    
    def get_min(self):
        return self.heap[0][1]
    
    def remove_min(self, flag):
        val = self.get_min()[3]
        self.remove(val, flag)

    
class ListNode:
    def __init__(self, item, next, prev):
        self.label = item[0]
        self.item = item
        self.next = next
        self.prev = prev
    
    def __str__(self):
        return ("(label=" + str(self.label) + ", item=" + str(self.item) + ")")
        
        
class CustomLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def __str__(self):
        curr = self.head
        if curr == None:
            return ""
        
        # first node has no arrow pointing to it
        LL_as_str = str(curr)
        curr = curr.next
        
        while curr != None:
            LL_as_str += " --> "
            LL_as_str += str(curr)
            curr = curr.next
    
        return LL_as_str
        
    def add_node(self, item):
        new = ListNode(item, None, self.tail)
        if self.head == None:
            self.head = new
        if self.tail != None:
            self.tail.next = new
        self.tail = new
        self.size += 1
            
        
    def register_use(self, label):
        curr = self.head
        while curr.label != label:
            curr = curr.next
        
        # now we have found item of interest, and curr points to it
        
        # chop item from list
        if curr.prev != None:
            curr.prev.next = curr.next
        if curr.next != None:
            curr.next.prev = curr.prev
        
        # place item at the end of the list to say it's most recently used
        self.tail.next = curr
        curr.prev = self.tail
        curr.next = None
        self.tail = curr
        
    def remove_least_recently_used(self, heap):
        # least recently used in stored in head
        lru = self.head
        if lru.next != None:
            lru.next.prev = None
        self.head = lru.next
        
        # SHOULD ALSO CHECK IF THIS MAKES LIST EMPTY, IN WHICH CASE WE REMOVE THE LL FROM HEAP
        self.size -= 1
        if self.size <= 0:
            # remove this priority node from priority heap
            priority = lru.item[2]
            heap.remove_list(priority)
        
        return lru


class PEC:
    def __init__(self, max_items):
        self.max_items = max_items
        self.curr_items = 0
        self.items = {}
        self.expire_time_heap = MinHeap()
        self.priority_heap = MinHeap()
        self.curr_time = 0
        
    def __str__(self):
        return str(self.items)
    
    def Set(self, label, value, priority, expire_time):
        # should evict an item if we don't have enough room to set
        # using a loop is more of a precaution, we should never have more than max_items in the cache
        while self.curr_items >= self.max_items:
            self.evict()
            self.curr_items -= 1
        
        # now we are guaranteed to have enough room to put the item in
        # so put the item in the cache
        new_item = (label, value, priority, expire_time)
        self.items[label] = new_item
        self.expire_time_heap.insert(new_item, "expire heap")
        self.priority_heap.insert(new_item, "priority heap")
        self.curr_items += 1
    
    def Get(self, label):
        if label not in self.items:
            return "Error: item with this label not in cache"
        
        retrieved_item =  self.items[label]
        
        # now we need to register that this item is recently used
        retrieved_item_priority_list = self.priority_heap.priority_map[retrieved_item[2]]
        retrieved_item_priority_list.register_use(label)
        
        # now we can return the item
        return self.items[label]
    
    def evict(self):
        # first see if any items are expired and remove if so
        min_expire_item = self.expire_time_heap.get_min()
        min_expire_time = min_expire_item[3]
        
        if min_expire_time < self.curr_time:
            self.expire_time_heap.remove_min("expire heap")    # item is expire, remove from expire_time heap
            self.priority_heap.remove(min_expire_item, "priority heap")    # also need to remove the item from other heap
            
            # for thing in self.priority_heap.heap:
            #     print(str(thing[0]) + ": " + str(thing[1]))
                
            del self.items[min_expire_item[0]]    # remove the item from cache
            self.curr_items -= 1
            return    # we evicted an item, so we return immediately
        
        # if not, grab min priority items list
        min_priority_list = self.priority_heap.get_min()
        lru = min_priority_list.remove_least_recently_used(self.priority_heap)
        self.expire_time_heap.remove(lru, "expire heap")    # remove the item from other heap
        del self.items[lru.label]    # remove the item from cache
        self.curr_items -= 1
        return    # we evicted an item, so we return immediately
    
    def set_max_items(self, n):
        self.max_items = n
        while self.curr_items > self.max_items:
            self.evict()
            

##############       
# Zack's Tests
##############
# pec = PEC(5)
# pec.Set("A", 3, 5, 10)
# print(pec.Get("A"))
# pec.evict()
# print(pec)

##############       
# Given Tests
##############
c = PEC(5)
c.Set("A", 1, 5, 100)


c.Set("B", 2, 15, 3)


c.Set("C", 3, 5, 10)


c.Set("D", 4, 1, 15)


c.Set("E", 5, 5, 150)

c.Get("C")

# a quick test for error handling
print("This should throw an error as an example of error handling. I would love to implement more error handling at a future date when I have time.")
print(c.Get("F"))
print()

# // Current time = 0
# c.SetMaxItems(5)
# c.Keys() = ["A", "B", "C", "D", "E"]
# // space for 5 keys, all 5 items are included
# 
c.curr_time = 5
# 
# // Current time = 5
c.set_max_items(4)
# c.Keys() = ["A", "C", "D", "E"]
# // "B" is removed because it is expired.  e3 < e5
#
print(c)
c.set_max_items(3)
# c.Keys() = ["A", "C", "E"]
# // "D" is removed because it the lowest priority
# // D's expire time is irrelevant.
# 
print(c)
c.set_max_items(2)
# c.Keys() = ["C", "E"]
# // "A" is removed because it is least recently used."
# // A's expire time is irrelevant.
# 
print(c)
c.set_max_items(1)
# c.Keys() = ["C"]
# // "E" is removed because C is more recently used (due to the Get("C") event).
print("At this point our cache should only have C")
print(c)
