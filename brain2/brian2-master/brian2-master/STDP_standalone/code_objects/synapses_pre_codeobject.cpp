#include "code_objects/synapses_pre_codeobject.h"
#include "objects.h"
#include "brianlib/common_math.h"
#include "brianlib/stdint_compat.h"
#include<cmath>
#include<ctime>
#include<iostream>
#include<fstream>
#include<climits>
#include "brianlib/stdint_compat.h"
#include "synapses_classes.h"

////// SUPPORT CODE ///////
namespace {
        
    template <typename T>
    static inline T _clip(const T value, const double a_min, const double a_max)
    {
        if (value < a_min)
            return a_min;
        if (value > a_max)
            return a_max;
        return value;
    }
    template < typename T1, typename T2 > struct _higher_type;
    template < > struct _higher_type<int,int> { typedef int type; };
    template < > struct _higher_type<int,long> { typedef long type; };
    template < > struct _higher_type<int,long long> { typedef long long type; };
    template < > struct _higher_type<int,float> { typedef float type; };
    template < > struct _higher_type<int,double> { typedef double type; };
    template < > struct _higher_type<int,long double> { typedef long double type; };
    template < > struct _higher_type<long,int> { typedef long type; };
    template < > struct _higher_type<long,long> { typedef long type; };
    template < > struct _higher_type<long,long long> { typedef long long type; };
    template < > struct _higher_type<long,float> { typedef float type; };
    template < > struct _higher_type<long,double> { typedef double type; };
    template < > struct _higher_type<long,long double> { typedef long double type; };
    template < > struct _higher_type<long long,int> { typedef long long type; };
    template < > struct _higher_type<long long,long> { typedef long long type; };
    template < > struct _higher_type<long long,long long> { typedef long long type; };
    template < > struct _higher_type<long long,float> { typedef float type; };
    template < > struct _higher_type<long long,double> { typedef double type; };
    template < > struct _higher_type<long long,long double> { typedef long double type; };
    template < > struct _higher_type<float,int> { typedef float type; };
    template < > struct _higher_type<float,long> { typedef float type; };
    template < > struct _higher_type<float,long long> { typedef float type; };
    template < > struct _higher_type<float,float> { typedef float type; };
    template < > struct _higher_type<float,double> { typedef double type; };
    template < > struct _higher_type<float,long double> { typedef long double type; };
    template < > struct _higher_type<double,int> { typedef double type; };
    template < > struct _higher_type<double,long> { typedef double type; };
    template < > struct _higher_type<double,long long> { typedef double type; };
    template < > struct _higher_type<double,float> { typedef double type; };
    template < > struct _higher_type<double,double> { typedef double type; };
    template < > struct _higher_type<double,long double> { typedef long double type; };
    template < > struct _higher_type<long double,int> { typedef long double type; };
    template < > struct _higher_type<long double,long> { typedef long double type; };
    template < > struct _higher_type<long double,long long> { typedef long double type; };
    template < > struct _higher_type<long double,float> { typedef long double type; };
    template < > struct _higher_type<long double,double> { typedef long double type; };
    template < > struct _higher_type<long double,long double> { typedef long double type; };
    template < typename T1, typename T2 >
    static inline typename _higher_type<T1,T2>::type
    _brian_mod(T1 x, T2 y)
    {{
        return x-y*floor(1.0*x/y);
    }}
    template < typename T1, typename T2 >
    static inline typename _higher_type<T1,T2>::type
    _brian_floordiv(T1 x, T2 y)
    {{
        return floor(1.0*x/y);
    }}
    #ifdef _MSC_VER
    #define _brian_pow(x, y) (pow((double)(x), (y)))
    #else
    #define _brian_pow(x, y) (pow((x), (y)))
    #endif

}

////// HASH DEFINES ///////



void _run_synapses_pre_codeobject()
{
    using namespace brian;


    ///// CONSTANTS ///////////
    double* const _array_synapses_Apost = _dynamic_array_synapses_Apost.empty()? 0 : &_dynamic_array_synapses_Apost[0];
const size_t _numApost = _dynamic_array_synapses_Apost.size();
double* const _array_synapses_Apre = _dynamic_array_synapses_Apre.empty()? 0 : &_dynamic_array_synapses_Apre[0];
const size_t _numApre = _dynamic_array_synapses_Apre.size();
int32_t* const _array_synapses__synaptic_pre = _dynamic_array_synapses__synaptic_pre.empty()? 0 : &_dynamic_array_synapses__synaptic_pre[0];
const size_t _num_synaptic_pre = _dynamic_array_synapses__synaptic_pre.size();
const double dApre = 0.0001;
const size_t _numge = 1;
const double gmax = 0.01;
double* const _array_synapses_lastupdate = _dynamic_array_synapses_lastupdate.empty()? 0 : &_dynamic_array_synapses_lastupdate[0];
const size_t _numlastupdate = _dynamic_array_synapses_lastupdate.size();
const size_t _numt = 1;
const double taupost = 0.02;
const double taupre = 0.02;
double* const _array_synapses_w = _dynamic_array_synapses_w.empty()? 0 : &_dynamic_array_synapses_w[0];
const size_t _numw = _dynamic_array_synapses_w.size();
int32_t* const _array_synapses__synaptic_post = _dynamic_array_synapses__synaptic_post.empty()? 0 : &_dynamic_array_synapses__synaptic_post[0];
const size_t _num_postsynaptic_idx = _dynamic_array_synapses__synaptic_post.size();
    ///// POINTERS ////////////
        
    double* __restrict  _ptr_array_synapses_Apost = _array_synapses_Apost;
    double* __restrict  _ptr_array_synapses_Apre = _array_synapses_Apre;
    int32_t* __restrict  _ptr_array_synapses__synaptic_pre = _array_synapses__synaptic_pre;
    double*   _ptr_array_neurongroup_ge = _array_neurongroup_ge;
    double* __restrict  _ptr_array_synapses_lastupdate = _array_synapses_lastupdate;
    double*   _ptr_array_defaultclock_t = _array_defaultclock_t;
    double* __restrict  _ptr_array_synapses_w = _array_synapses_w;
    int32_t* __restrict  _ptr_array_synapses__synaptic_post = _array_synapses__synaptic_post;



    // This is only needed for the _debugmsg function below

    // scalar code
    const size_t _vectorisation_idx = -1;
        
    const double t = _ptr_array_defaultclock_t[0];
    const double _lio_1 = 1.0f*1.0/taupost;
    const double _lio_2 = 1.0f*1.0/taupre;


    
    {
    std::vector<int> *_spiking_synapses = synapses_pre.peek();
    const int _num_spiking_synapses = _spiking_synapses->size();

    
    {
        for(int _spiking_synapse_idx=0;
            _spiking_synapse_idx<_num_spiking_synapses;
            _spiking_synapse_idx++)
        {
            const size_t _idx = (*_spiking_synapses)[_spiking_synapse_idx];
            const size_t _vectorisation_idx = _idx;
                        
            const int32_t _postsynaptic_idx = _ptr_array_synapses__synaptic_post[_idx];
            double Apost = _ptr_array_synapses_Apost[_idx];
            double Apre = _ptr_array_synapses_Apre[_idx];
            double ge = _ptr_array_neurongroup_ge[_postsynaptic_idx];
            double lastupdate = _ptr_array_synapses_lastupdate[_idx];
            double w = _ptr_array_synapses_w[_idx];
            const double _Apost = Apost * exp(_lio_1 * (- (t - lastupdate)));
            const double _Apre = Apre * exp(_lio_2 * (- (t - lastupdate)));
            Apost = _Apost;
            Apre = _Apre;
            ge += w;
            Apre += dApre;
            w = _clip(w + Apost, 0, gmax);
            lastupdate = t;
            _ptr_array_synapses_Apost[_idx] = Apost;
            _ptr_array_synapses_Apre[_idx] = Apre;
            _ptr_array_neurongroup_ge[_postsynaptic_idx] = ge;
            _ptr_array_synapses_lastupdate[_idx] = lastupdate;
            _ptr_array_synapses_w[_idx] = w;

        }
    }
    }

}

void _debugmsg_synapses_pre_codeobject()
{
    using namespace brian;
    std::cout << "Number of synapses: " << _dynamic_array_synapses__synaptic_pre.size() << endl;
}

