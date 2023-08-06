from shared_atomic.atomic_object_backend cimport atomic_object

cpdef str string_get_string(atomic_string string)
cpdef void string_set_string(atomic_string string, str data) except *
cpdef str string_get_and_set(atomic_string string, str data)
cpdef str string_compare_and_set_value(atomic_string string, str i, str n)
cpdef void string_store(atomic_string n, atomic_string i) except *
cpdef void string_shift(atomic_string n, atomic_string i, atomic_string j) except *
cpdef bint string_compare_and_set(atomic_string j, atomic_string i, str n) except *

cdef class atomic_string(atomic_object):
    """
    string provide atomic operations, the string should be no longer than 8 bytes
    :attributes
        encoding: readonly string character set\n
        size: readonly size of the string\n
        initial_byte_length: readonly initial input length as number of bytes it took\n
        value: read/write value of the string\n
        mode: readonly 's' for single process, 'm' for multiprocessing, on windows platform, only singleprocessing is supported\n
        windows_unix_compatibility: readonly whether the source code should be compatible with windows x64
    """

    cdef readonly str x6
    cdef readonly char x7
    cdef char x8
    #cdef dict internal_type


    cpdef str get_string(self)
    cpdef void set_string(self, str data) except *
    cpdef str string_compare_and_set_value(self, str i, str n)
    cpdef str string_get_and_set(self, str data)
    cpdef void string_store(self, atomic_string i) except *
    cpdef void string_shift(self, atomic_string i, atomic_string j) except *
    cpdef bint string_compare_and_set(self, atomic_string i, str n) except *
    cpdef void resize(self, char newlength,
                str paddingdirection = *,
                str paddingstr  = *,
                str trimming_direction  = *) except *
    cpdef void reencode(self, str newencode) except *
