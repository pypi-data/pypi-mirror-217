# -*- coding: utf-8 -*-
import pathlib
from ctypes import CDLL, POINTER, c_char_p, c_float, c_int32, c_void_p

library_path = pathlib.Path(__file__).parent.resolve() / "libggml-bindings.so"
shared_lib = CDLL(str(library_path))


# Falcon
shared_lib.falcon_load_model.argtypes = [c_char_p]
shared_lib.falcon_load_model.restype = c_void_p

shared_lib.falcon_free_model.argtypes = [c_void_p]
shared_lib.falcon_free_model.restype = c_int32

shared_lib.falcon_generate.argtypes = [
    c_void_p,  # model
    POINTER(c_int32),  # input tokens array
    c_int32,  # input tokens length
    POINTER(c_int32),  # output tokens array
    c_int32,  # n_predict
    c_int32,  # n_threads
    c_int32,  # seed
    c_int32,  # n_batch
    c_int32,  # top_k
    c_float,  # top_p
    c_float,  # temp
]
shared_lib.falcon_generate.restype = c_int32

# GPT-NeoX
shared_lib.gpt_neox_load_model.argtypes = [c_char_p]
shared_lib.gpt_neox_load_model.restype = c_void_p

shared_lib.gpt_neox_free_model.argtypes = [c_void_p]
shared_lib.gpt_neox_free_model.restype = c_int32

shared_lib.gpt_neox_generate.argtypes = [
    c_void_p,  # model
    POINTER(c_int32),  # input tokens array
    c_int32,  # input tokens length
    POINTER(c_int32),  # output tokens array
    c_int32,  # n_predict
    c_int32,  # n_threads
    c_int32,  # seed
    c_int32,  # n_batch
    c_int32,  # top_k
    c_float,  # top_p
    c_float,  # temp
]
shared_lib.gpt_neox_generate.restype = c_int32

# MPT
shared_lib.mpt_load_model.argtypes = [c_char_p]
shared_lib.mpt_load_model.restype = c_void_p

shared_lib.mpt_free_model.argtypes = [c_void_p]
shared_lib.mpt_free_model.restype = c_int32

shared_lib.mpt_generate.argtypes = [
    c_void_p,  # model
    POINTER(c_int32),  # input tokens array
    c_int32,  # input tokens length
    POINTER(c_int32),  # output tokens array
    c_int32,  # n_predict
    c_int32,  # n_threads
    c_int32,  # seed
    c_int32,  # n_batch
    c_int32,  # top_k
    c_float,  # top_p
    c_float,  # temp
]
shared_lib.mpt_generate.restype = c_int32
