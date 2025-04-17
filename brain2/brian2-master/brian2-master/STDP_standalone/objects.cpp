

#include "objects.h"
#include "synapses_classes.h"
#include "brianlib/clocks.h"
#include "brianlib/dynamic_array.h"
#include "brianlib/stdint_compat.h"
#include "network.h"
#include "randomkit.h"
#include<vector>
#include<iostream>
#include<fstream>
#include<map>
#include<tuple>
#include<cstdlib>
#include<string>

namespace brian {

std::string results_dir = "results/";  // can be overwritten by --results_dir command line arg
std::vector< rk_state* > _mersenne_twister_states;

//////////////// networks /////////////////
Network magicnetwork;

void set_variable_from_value(std::string varname, char* var_pointer, size_t size, char value) {
    #ifdef DEBUG
    std::cout << "Setting '" << varname << "' to " << (value == 1 ? "True" : "False") << std::endl;
    #endif
    std::fill(var_pointer, var_pointer+size, value);
}

template<class T> void set_variable_from_value(std::string varname, T* var_pointer, size_t size, T value) {
    #ifdef DEBUG
    std::cout << "Setting '" << varname << "' to " << value << std::endl;
    #endif
    std::fill(var_pointer, var_pointer+size, value);
}

template<class T> void set_variable_from_file(std::string varname, T* var_pointer, size_t data_size, std::string filename) {
    ifstream f;
    streampos size;
    #ifdef DEBUG
    std::cout << "Setting '" << varname << "' from file '" << filename << "'" << std::endl;
    #endif
    f.open(filename, ios::in | ios::binary | ios::ate);
    size = f.tellg();
    if (size != data_size) {
        std::cerr << "Error reading '" << filename << "': file size " << size << " does not match expected size " << data_size << std::endl;
        return;
    }
    f.seekg(0, ios::beg);
    if (f.is_open())
        f.read(reinterpret_cast<char *>(var_pointer), data_size);
    else
        std::cerr << "Could not read '" << filename << "'" << std::endl;
    if (f.fail())
        std::cerr << "Error reading '" << filename << "'" << std::endl;
}

//////////////// set arrays by name ///////
void set_variable_by_name(std::string name, std::string s_value) {
	size_t var_size;
	size_t data_size;
	std::for_each(s_value.begin(), s_value.end(), [](char& c) // modify in-place
    {
        c = std::tolower(static_cast<unsigned char>(c));
    });
    if (s_value == "true")
        s_value = "1";
    else if (s_value == "false")
        s_value = "0";
	// non-dynamic arrays
    if (name == "neurongroup._spikespace") {
        var_size = 2;
        data_size = 2*sizeof(int32_t);
        if (s_value[0] == '-' || (s_value[0] >= '0' && s_value[0] <= '9')) {
            // set from single value
            set_variable_from_value<int32_t>(name, _array_neurongroup__spikespace, var_size, (int32_t)atoi(s_value.c_str()));

        } else {
            // set from file
            set_variable_from_file(name, _array_neurongroup__spikespace, data_size, s_value);
        }
        return;
    }
    if (name == "neurongroup.ge") {
        var_size = 1;
        data_size = 1*sizeof(double);
        if (s_value[0] == '-' || (s_value[0] >= '0' && s_value[0] <= '9')) {
            // set from single value
            set_variable_from_value<double>(name, _array_neurongroup_ge, var_size, (double)atof(s_value.c_str()));

        } else {
            // set from file
            set_variable_from_file(name, _array_neurongroup_ge, data_size, s_value);
        }
        return;
    }
    if (name == "neurongroup.v") {
        var_size = 1;
        data_size = 1*sizeof(double);
        if (s_value[0] == '-' || (s_value[0] >= '0' && s_value[0] <= '9')) {
            // set from single value
            set_variable_from_value<double>(name, _array_neurongroup_v, var_size, (double)atof(s_value.c_str()));

        } else {
            // set from file
            set_variable_from_file(name, _array_neurongroup_v, data_size, s_value);
        }
        return;
    }
    if (name == "poissongroup._spikespace") {
        var_size = 1001;
        data_size = 1001*sizeof(int32_t);
        if (s_value[0] == '-' || (s_value[0] >= '0' && s_value[0] <= '9')) {
            // set from single value
            set_variable_from_value<int32_t>(name, _array_poissongroup__spikespace, var_size, (int32_t)atoi(s_value.c_str()));

        } else {
            // set from file
            set_variable_from_file(name, _array_poissongroup__spikespace, data_size, s_value);
        }
        return;
    }
    if (name == "poissongroup.rates") {
        var_size = 1000;
        data_size = 1000*sizeof(double);
        if (s_value[0] == '-' || (s_value[0] >= '0' && s_value[0] <= '9')) {
            // set from single value
            set_variable_from_value<double>(name, _array_poissongroup_rates, var_size, (double)atof(s_value.c_str()));

        } else {
            // set from file
            set_variable_from_file(name, _array_poissongroup_rates, data_size, s_value);
        }
        return;
    }
    // dynamic arrays (1d)
    if (name == "synapses.Apost") {
        var_size = _dynamic_array_synapses_Apost.size();
        data_size = var_size*sizeof(double);
        if (s_value[0] == '-' || (s_value[0] >= '0' && s_value[0] <= '9')) {
            // set from single value
            set_variable_from_value<double>(name, &_dynamic_array_synapses_Apost[0], var_size, (double)atof(s_value.c_str()));

        } else {
            // set from file
            set_variable_from_file(name, &_dynamic_array_synapses_Apost[0], data_size, s_value);
        }
        return;
    }
    if (name == "synapses.Apre") {
        var_size = _dynamic_array_synapses_Apre.size();
        data_size = var_size*sizeof(double);
        if (s_value[0] == '-' || (s_value[0] >= '0' && s_value[0] <= '9')) {
            // set from single value
            set_variable_from_value<double>(name, &_dynamic_array_synapses_Apre[0], var_size, (double)atof(s_value.c_str()));

        } else {
            // set from file
            set_variable_from_file(name, &_dynamic_array_synapses_Apre[0], data_size, s_value);
        }
        return;
    }
    if (name == "synapses.delay") {
        var_size = _dynamic_array_synapses_delay.size();
        data_size = var_size*sizeof(double);
        if (s_value[0] == '-' || (s_value[0] >= '0' && s_value[0] <= '9')) {
            // set from single value
            set_variable_from_value<double>(name, &_dynamic_array_synapses_delay[0], var_size, (double)atof(s_value.c_str()));

        } else {
            // set from file
            set_variable_from_file(name, &_dynamic_array_synapses_delay[0], data_size, s_value);
        }
        return;
    }
    if (name == "synapses.delay") {
        var_size = _dynamic_array_synapses_delay_1.size();
        data_size = var_size*sizeof(double);
        if (s_value[0] == '-' || (s_value[0] >= '0' && s_value[0] <= '9')) {
            // set from single value
            set_variable_from_value<double>(name, &_dynamic_array_synapses_delay_1[0], var_size, (double)atof(s_value.c_str()));

        } else {
            // set from file
            set_variable_from_file(name, &_dynamic_array_synapses_delay_1[0], data_size, s_value);
        }
        return;
    }
    if (name == "synapses.lastupdate") {
        var_size = _dynamic_array_synapses_lastupdate.size();
        data_size = var_size*sizeof(double);
        if (s_value[0] == '-' || (s_value[0] >= '0' && s_value[0] <= '9')) {
            // set from single value
            set_variable_from_value<double>(name, &_dynamic_array_synapses_lastupdate[0], var_size, (double)atof(s_value.c_str()));

        } else {
            // set from file
            set_variable_from_file(name, &_dynamic_array_synapses_lastupdate[0], data_size, s_value);
        }
        return;
    }
    if (name == "synapses.w") {
        var_size = _dynamic_array_synapses_w.size();
        data_size = var_size*sizeof(double);
        if (s_value[0] == '-' || (s_value[0] >= '0' && s_value[0] <= '9')) {
            // set from single value
            set_variable_from_value<double>(name, &_dynamic_array_synapses_w[0], var_size, (double)atof(s_value.c_str()));

        } else {
            // set from file
            set_variable_from_file(name, &_dynamic_array_synapses_w[0], data_size, s_value);
        }
        return;
    }
    std::cerr << "Cannot set unknown variable '" << name << "'." << std::endl;
    exit(1);
}
//////////////// arrays ///////////////////
double * _array_defaultclock_dt;
const int _num__array_defaultclock_dt = 1;
double * _array_defaultclock_t;
const int _num__array_defaultclock_t = 1;
int64_t * _array_defaultclock_timestep;
const int _num__array_defaultclock_timestep = 1;
int32_t * _array_neurongroup__spikespace;
const int _num__array_neurongroup__spikespace = 2;
double * _array_neurongroup_ge;
const int _num__array_neurongroup_ge = 1;
int32_t * _array_neurongroup_i;
const int _num__array_neurongroup_i = 1;
double * _array_neurongroup_v;
const int _num__array_neurongroup_v = 1;
int32_t * _array_poissongroup__spikespace;
const int _num__array_poissongroup__spikespace = 1001;
int32_t * _array_poissongroup_i;
const int _num__array_poissongroup_i = 1000;
double * _array_poissongroup_rates;
const int _num__array_poissongroup_rates = 1000;
int32_t * _array_spikemonitor__source_idx;
const int _num__array_spikemonitor__source_idx = 1000;
int32_t * _array_spikemonitor_count;
const int _num__array_spikemonitor_count = 1000;
int32_t * _array_spikemonitor_N;
const int _num__array_spikemonitor_N = 1;
int32_t * _array_statemonitor__indices;
const int _num__array_statemonitor__indices = 2;
int32_t * _array_statemonitor_N;
const int _num__array_statemonitor_N = 1;
double * _array_statemonitor_w;
const int _num__array_statemonitor_w = (0, 2);
int32_t * _array_synapses_N;
const int _num__array_synapses_N = 1;

//////////////// dynamic arrays 1d /////////
std::vector<int32_t> _dynamic_array_spikemonitor_i;
std::vector<double> _dynamic_array_spikemonitor_t;
std::vector<double> _dynamic_array_statemonitor_t;
std::vector<int32_t> _dynamic_array_synapses__synaptic_post;
std::vector<int32_t> _dynamic_array_synapses__synaptic_pre;
std::vector<double> _dynamic_array_synapses_Apost;
std::vector<double> _dynamic_array_synapses_Apre;
std::vector<double> _dynamic_array_synapses_delay;
std::vector<double> _dynamic_array_synapses_delay_1;
std::vector<double> _dynamic_array_synapses_lastupdate;
std::vector<int32_t> _dynamic_array_synapses_N_incoming;
std::vector<int32_t> _dynamic_array_synapses_N_outgoing;
std::vector<double> _dynamic_array_synapses_w;

//////////////// dynamic arrays 2d /////////
DynamicArray2D<double> _dynamic_array_statemonitor_w;

/////////////// static arrays /////////////
int32_t * _static_array__array_statemonitor__indices;
const int _num__static_array__array_statemonitor__indices = 2;

//////////////// synapses /////////////////
// synapses
SynapticPathway synapses_post(
		_dynamic_array_synapses__synaptic_post,
		0, 1);
SynapticPathway synapses_pre(
		_dynamic_array_synapses__synaptic_pre,
		0, 1000);

//////////////// clocks ///////////////////
Clock defaultclock;  // attributes will be set in run.cpp

// Profiling information for each code object
}

void _init_arrays()
{
	using namespace brian;

    // Arrays initialized to 0
	_array_defaultclock_dt = new double[1];
    
	for(int i=0; i<1; i++) _array_defaultclock_dt[i] = 0;

	_array_defaultclock_t = new double[1];
    
	for(int i=0; i<1; i++) _array_defaultclock_t[i] = 0;

	_array_defaultclock_timestep = new int64_t[1];
    
	for(int i=0; i<1; i++) _array_defaultclock_timestep[i] = 0;

	_array_neurongroup__spikespace = new int32_t[2];
    
	for(int i=0; i<2; i++) _array_neurongroup__spikespace[i] = 0;

	_array_neurongroup_ge = new double[1];
    
	for(int i=0; i<1; i++) _array_neurongroup_ge[i] = 0;

	_array_neurongroup_i = new int32_t[1];
    
	for(int i=0; i<1; i++) _array_neurongroup_i[i] = 0;

	_array_neurongroup_v = new double[1];
    
	for(int i=0; i<1; i++) _array_neurongroup_v[i] = 0;

	_array_poissongroup__spikespace = new int32_t[1001];
    
	for(int i=0; i<1001; i++) _array_poissongroup__spikespace[i] = 0;

	_array_poissongroup_i = new int32_t[1000];
    
	for(int i=0; i<1000; i++) _array_poissongroup_i[i] = 0;

	_array_poissongroup_rates = new double[1000];
    
	for(int i=0; i<1000; i++) _array_poissongroup_rates[i] = 0;

	_array_spikemonitor__source_idx = new int32_t[1000];
    
	for(int i=0; i<1000; i++) _array_spikemonitor__source_idx[i] = 0;

	_array_spikemonitor_count = new int32_t[1000];
    
	for(int i=0; i<1000; i++) _array_spikemonitor_count[i] = 0;

	_array_spikemonitor_N = new int32_t[1];
    
	for(int i=0; i<1; i++) _array_spikemonitor_N[i] = 0;

	_array_statemonitor__indices = new int32_t[2];
    
	for(int i=0; i<2; i++) _array_statemonitor__indices[i] = 0;

	_array_statemonitor_N = new int32_t[1];
    
	for(int i=0; i<1; i++) _array_statemonitor_N[i] = 0;

	_array_synapses_N = new int32_t[1];
    
	for(int i=0; i<1; i++) _array_synapses_N[i] = 0;


	// Arrays initialized to an "arange"
	_array_neurongroup_i = new int32_t[1];
    
	for(int i=0; i<1; i++) _array_neurongroup_i[i] = 0 + i;

	_array_poissongroup_i = new int32_t[1000];
    
	for(int i=0; i<1000; i++) _array_poissongroup_i[i] = 0 + i;

	_array_spikemonitor__source_idx = new int32_t[1000];
    
	for(int i=0; i<1000; i++) _array_spikemonitor__source_idx[i] = 0 + i;


	// static arrays
	_static_array__array_statemonitor__indices = new int32_t[2];

	// Random number generator states
	for (int i=0; i<1; i++)
	    _mersenne_twister_states.push_back(new rk_state());
}

void _load_arrays()
{
	using namespace brian;

	ifstream f_static_array__array_statemonitor__indices;
	f_static_array__array_statemonitor__indices.open("static_arrays/_static_array__array_statemonitor__indices", ios::in | ios::binary);
	if(f_static_array__array_statemonitor__indices.is_open())
	{
		f_static_array__array_statemonitor__indices.read(reinterpret_cast<char*>(_static_array__array_statemonitor__indices), 2*sizeof(int32_t));
	} else
	{
		std::cout << "Error opening static array _static_array__array_statemonitor__indices." << endl;
	}
}

void _write_arrays()
{
	using namespace brian;

	ofstream outfile__array_defaultclock_dt;
	outfile__array_defaultclock_dt.open(results_dir + "_array_defaultclock_dt_1978099143", ios::binary | ios::out);
	if(outfile__array_defaultclock_dt.is_open())
	{
		outfile__array_defaultclock_dt.write(reinterpret_cast<char*>(_array_defaultclock_dt), 1*sizeof(_array_defaultclock_dt[0]));
		outfile__array_defaultclock_dt.close();
	} else
	{
		std::cout << "Error writing output file for _array_defaultclock_dt." << endl;
	}
	ofstream outfile__array_defaultclock_t;
	outfile__array_defaultclock_t.open(results_dir + "_array_defaultclock_t_2669362164", ios::binary | ios::out);
	if(outfile__array_defaultclock_t.is_open())
	{
		outfile__array_defaultclock_t.write(reinterpret_cast<char*>(_array_defaultclock_t), 1*sizeof(_array_defaultclock_t[0]));
		outfile__array_defaultclock_t.close();
	} else
	{
		std::cout << "Error writing output file for _array_defaultclock_t." << endl;
	}
	ofstream outfile__array_defaultclock_timestep;
	outfile__array_defaultclock_timestep.open(results_dir + "_array_defaultclock_timestep_144223508", ios::binary | ios::out);
	if(outfile__array_defaultclock_timestep.is_open())
	{
		outfile__array_defaultclock_timestep.write(reinterpret_cast<char*>(_array_defaultclock_timestep), 1*sizeof(_array_defaultclock_timestep[0]));
		outfile__array_defaultclock_timestep.close();
	} else
	{
		std::cout << "Error writing output file for _array_defaultclock_timestep." << endl;
	}
	ofstream outfile__array_neurongroup__spikespace;
	outfile__array_neurongroup__spikespace.open(results_dir + "_array_neurongroup__spikespace_3522821529", ios::binary | ios::out);
	if(outfile__array_neurongroup__spikespace.is_open())
	{
		outfile__array_neurongroup__spikespace.write(reinterpret_cast<char*>(_array_neurongroup__spikespace), 2*sizeof(_array_neurongroup__spikespace[0]));
		outfile__array_neurongroup__spikespace.close();
	} else
	{
		std::cout << "Error writing output file for _array_neurongroup__spikespace." << endl;
	}
	ofstream outfile__array_neurongroup_ge;
	outfile__array_neurongroup_ge.open(results_dir + "_array_neurongroup_ge_2625384453", ios::binary | ios::out);
	if(outfile__array_neurongroup_ge.is_open())
	{
		outfile__array_neurongroup_ge.write(reinterpret_cast<char*>(_array_neurongroup_ge), 1*sizeof(_array_neurongroup_ge[0]));
		outfile__array_neurongroup_ge.close();
	} else
	{
		std::cout << "Error writing output file for _array_neurongroup_ge." << endl;
	}
	ofstream outfile__array_neurongroup_i;
	outfile__array_neurongroup_i.open(results_dir + "_array_neurongroup_i_2649026944", ios::binary | ios::out);
	if(outfile__array_neurongroup_i.is_open())
	{
		outfile__array_neurongroup_i.write(reinterpret_cast<char*>(_array_neurongroup_i), 1*sizeof(_array_neurongroup_i[0]));
		outfile__array_neurongroup_i.close();
	} else
	{
		std::cout << "Error writing output file for _array_neurongroup_i." << endl;
	}
	ofstream outfile__array_neurongroup_v;
	outfile__array_neurongroup_v.open(results_dir + "_array_neurongroup_v_283966581", ios::binary | ios::out);
	if(outfile__array_neurongroup_v.is_open())
	{
		outfile__array_neurongroup_v.write(reinterpret_cast<char*>(_array_neurongroup_v), 1*sizeof(_array_neurongroup_v[0]));
		outfile__array_neurongroup_v.close();
	} else
	{
		std::cout << "Error writing output file for _array_neurongroup_v." << endl;
	}
	ofstream outfile__array_poissongroup__spikespace;
	outfile__array_poissongroup__spikespace.open(results_dir + "_array_poissongroup__spikespace_1019000416", ios::binary | ios::out);
	if(outfile__array_poissongroup__spikespace.is_open())
	{
		outfile__array_poissongroup__spikespace.write(reinterpret_cast<char*>(_array_poissongroup__spikespace), 1001*sizeof(_array_poissongroup__spikespace[0]));
		outfile__array_poissongroup__spikespace.close();
	} else
	{
		std::cout << "Error writing output file for _array_poissongroup__spikespace." << endl;
	}
	ofstream outfile__array_poissongroup_i;
	outfile__array_poissongroup_i.open(results_dir + "_array_poissongroup_i_1277690444", ios::binary | ios::out);
	if(outfile__array_poissongroup_i.is_open())
	{
		outfile__array_poissongroup_i.write(reinterpret_cast<char*>(_array_poissongroup_i), 1000*sizeof(_array_poissongroup_i[0]));
		outfile__array_poissongroup_i.close();
	} else
	{
		std::cout << "Error writing output file for _array_poissongroup_i." << endl;
	}
	ofstream outfile__array_poissongroup_rates;
	outfile__array_poissongroup_rates.open(results_dir + "_array_poissongroup_rates_3353413371", ios::binary | ios::out);
	if(outfile__array_poissongroup_rates.is_open())
	{
		outfile__array_poissongroup_rates.write(reinterpret_cast<char*>(_array_poissongroup_rates), 1000*sizeof(_array_poissongroup_rates[0]));
		outfile__array_poissongroup_rates.close();
	} else
	{
		std::cout << "Error writing output file for _array_poissongroup_rates." << endl;
	}
	ofstream outfile__array_spikemonitor__source_idx;
	outfile__array_spikemonitor__source_idx.open(results_dir + "_array_spikemonitor__source_idx_1477951789", ios::binary | ios::out);
	if(outfile__array_spikemonitor__source_idx.is_open())
	{
		outfile__array_spikemonitor__source_idx.write(reinterpret_cast<char*>(_array_spikemonitor__source_idx), 1000*sizeof(_array_spikemonitor__source_idx[0]));
		outfile__array_spikemonitor__source_idx.close();
	} else
	{
		std::cout << "Error writing output file for _array_spikemonitor__source_idx." << endl;
	}
	ofstream outfile__array_spikemonitor_count;
	outfile__array_spikemonitor_count.open(results_dir + "_array_spikemonitor_count_598337445", ios::binary | ios::out);
	if(outfile__array_spikemonitor_count.is_open())
	{
		outfile__array_spikemonitor_count.write(reinterpret_cast<char*>(_array_spikemonitor_count), 1000*sizeof(_array_spikemonitor_count[0]));
		outfile__array_spikemonitor_count.close();
	} else
	{
		std::cout << "Error writing output file for _array_spikemonitor_count." << endl;
	}
	ofstream outfile__array_spikemonitor_N;
	outfile__array_spikemonitor_N.open(results_dir + "_array_spikemonitor_N_225734567", ios::binary | ios::out);
	if(outfile__array_spikemonitor_N.is_open())
	{
		outfile__array_spikemonitor_N.write(reinterpret_cast<char*>(_array_spikemonitor_N), 1*sizeof(_array_spikemonitor_N[0]));
		outfile__array_spikemonitor_N.close();
	} else
	{
		std::cout << "Error writing output file for _array_spikemonitor_N." << endl;
	}
	ofstream outfile__array_statemonitor__indices;
	outfile__array_statemonitor__indices.open(results_dir + "_array_statemonitor__indices_2854283999", ios::binary | ios::out);
	if(outfile__array_statemonitor__indices.is_open())
	{
		outfile__array_statemonitor__indices.write(reinterpret_cast<char*>(_array_statemonitor__indices), 2*sizeof(_array_statemonitor__indices[0]));
		outfile__array_statemonitor__indices.close();
	} else
	{
		std::cout << "Error writing output file for _array_statemonitor__indices." << endl;
	}
	ofstream outfile__array_statemonitor_N;
	outfile__array_statemonitor_N.open(results_dir + "_array_statemonitor_N_4140778434", ios::binary | ios::out);
	if(outfile__array_statemonitor_N.is_open())
	{
		outfile__array_statemonitor_N.write(reinterpret_cast<char*>(_array_statemonitor_N), 1*sizeof(_array_statemonitor_N[0]));
		outfile__array_statemonitor_N.close();
	} else
	{
		std::cout << "Error writing output file for _array_statemonitor_N." << endl;
	}
	ofstream outfile__array_synapses_N;
	outfile__array_synapses_N.open(results_dir + "_array_synapses_N_483293785", ios::binary | ios::out);
	if(outfile__array_synapses_N.is_open())
	{
		outfile__array_synapses_N.write(reinterpret_cast<char*>(_array_synapses_N), 1*sizeof(_array_synapses_N[0]));
		outfile__array_synapses_N.close();
	} else
	{
		std::cout << "Error writing output file for _array_synapses_N." << endl;
	}

	ofstream outfile__dynamic_array_spikemonitor_i;
	outfile__dynamic_array_spikemonitor_i.open(results_dir + "_dynamic_array_spikemonitor_i_1976709050", ios::binary | ios::out);
	if(outfile__dynamic_array_spikemonitor_i.is_open())
	{
        if (! _dynamic_array_spikemonitor_i.empty() )
        {
			outfile__dynamic_array_spikemonitor_i.write(reinterpret_cast<char*>(&_dynamic_array_spikemonitor_i[0]), _dynamic_array_spikemonitor_i.size()*sizeof(_dynamic_array_spikemonitor_i[0]));
		    outfile__dynamic_array_spikemonitor_i.close();
		}
	} else
	{
		std::cout << "Error writing output file for _dynamic_array_spikemonitor_i." << endl;
	}
	ofstream outfile__dynamic_array_spikemonitor_t;
	outfile__dynamic_array_spikemonitor_t.open(results_dir + "_dynamic_array_spikemonitor_t_383009635", ios::binary | ios::out);
	if(outfile__dynamic_array_spikemonitor_t.is_open())
	{
        if (! _dynamic_array_spikemonitor_t.empty() )
        {
			outfile__dynamic_array_spikemonitor_t.write(reinterpret_cast<char*>(&_dynamic_array_spikemonitor_t[0]), _dynamic_array_spikemonitor_t.size()*sizeof(_dynamic_array_spikemonitor_t[0]));
		    outfile__dynamic_array_spikemonitor_t.close();
		}
	} else
	{
		std::cout << "Error writing output file for _dynamic_array_spikemonitor_t." << endl;
	}
	ofstream outfile__dynamic_array_statemonitor_t;
	outfile__dynamic_array_statemonitor_t.open(results_dir + "_dynamic_array_statemonitor_t_3983503110", ios::binary | ios::out);
	if(outfile__dynamic_array_statemonitor_t.is_open())
	{
        if (! _dynamic_array_statemonitor_t.empty() )
        {
			outfile__dynamic_array_statemonitor_t.write(reinterpret_cast<char*>(&_dynamic_array_statemonitor_t[0]), _dynamic_array_statemonitor_t.size()*sizeof(_dynamic_array_statemonitor_t[0]));
		    outfile__dynamic_array_statemonitor_t.close();
		}
	} else
	{
		std::cout << "Error writing output file for _dynamic_array_statemonitor_t." << endl;
	}
	ofstream outfile__dynamic_array_synapses__synaptic_post;
	outfile__dynamic_array_synapses__synaptic_post.open(results_dir + "_dynamic_array_synapses__synaptic_post_1801389495", ios::binary | ios::out);
	if(outfile__dynamic_array_synapses__synaptic_post.is_open())
	{
        if (! _dynamic_array_synapses__synaptic_post.empty() )
        {
			outfile__dynamic_array_synapses__synaptic_post.write(reinterpret_cast<char*>(&_dynamic_array_synapses__synaptic_post[0]), _dynamic_array_synapses__synaptic_post.size()*sizeof(_dynamic_array_synapses__synaptic_post[0]));
		    outfile__dynamic_array_synapses__synaptic_post.close();
		}
	} else
	{
		std::cout << "Error writing output file for _dynamic_array_synapses__synaptic_post." << endl;
	}
	ofstream outfile__dynamic_array_synapses__synaptic_pre;
	outfile__dynamic_array_synapses__synaptic_pre.open(results_dir + "_dynamic_array_synapses__synaptic_pre_814148175", ios::binary | ios::out);
	if(outfile__dynamic_array_synapses__synaptic_pre.is_open())
	{
        if (! _dynamic_array_synapses__synaptic_pre.empty() )
        {
			outfile__dynamic_array_synapses__synaptic_pre.write(reinterpret_cast<char*>(&_dynamic_array_synapses__synaptic_pre[0]), _dynamic_array_synapses__synaptic_pre.size()*sizeof(_dynamic_array_synapses__synaptic_pre[0]));
		    outfile__dynamic_array_synapses__synaptic_pre.close();
		}
	} else
	{
		std::cout << "Error writing output file for _dynamic_array_synapses__synaptic_pre." << endl;
	}
	ofstream outfile__dynamic_array_synapses_Apost;
	outfile__dynamic_array_synapses_Apost.open(results_dir + "_dynamic_array_synapses_Apost_2876048651", ios::binary | ios::out);
	if(outfile__dynamic_array_synapses_Apost.is_open())
	{
        if (! _dynamic_array_synapses_Apost.empty() )
        {
			outfile__dynamic_array_synapses_Apost.write(reinterpret_cast<char*>(&_dynamic_array_synapses_Apost[0]), _dynamic_array_synapses_Apost.size()*sizeof(_dynamic_array_synapses_Apost[0]));
		    outfile__dynamic_array_synapses_Apost.close();
		}
	} else
	{
		std::cout << "Error writing output file for _dynamic_array_synapses_Apost." << endl;
	}
	ofstream outfile__dynamic_array_synapses_Apre;
	outfile__dynamic_array_synapses_Apre.open(results_dir + "_dynamic_array_synapses_Apre_3102407472", ios::binary | ios::out);
	if(outfile__dynamic_array_synapses_Apre.is_open())
	{
        if (! _dynamic_array_synapses_Apre.empty() )
        {
			outfile__dynamic_array_synapses_Apre.write(reinterpret_cast<char*>(&_dynamic_array_synapses_Apre[0]), _dynamic_array_synapses_Apre.size()*sizeof(_dynamic_array_synapses_Apre[0]));
		    outfile__dynamic_array_synapses_Apre.close();
		}
	} else
	{
		std::cout << "Error writing output file for _dynamic_array_synapses_Apre." << endl;
	}
	ofstream outfile__dynamic_array_synapses_delay;
	outfile__dynamic_array_synapses_delay.open(results_dir + "_dynamic_array_synapses_delay_3246960869", ios::binary | ios::out);
	if(outfile__dynamic_array_synapses_delay.is_open())
	{
        if (! _dynamic_array_synapses_delay.empty() )
        {
			outfile__dynamic_array_synapses_delay.write(reinterpret_cast<char*>(&_dynamic_array_synapses_delay[0]), _dynamic_array_synapses_delay.size()*sizeof(_dynamic_array_synapses_delay[0]));
		    outfile__dynamic_array_synapses_delay.close();
		}
	} else
	{
		std::cout << "Error writing output file for _dynamic_array_synapses_delay." << endl;
	}
	ofstream outfile__dynamic_array_synapses_delay_1;
	outfile__dynamic_array_synapses_delay_1.open(results_dir + "_dynamic_array_synapses_delay_1_3310102259", ios::binary | ios::out);
	if(outfile__dynamic_array_synapses_delay_1.is_open())
	{
        if (! _dynamic_array_synapses_delay_1.empty() )
        {
			outfile__dynamic_array_synapses_delay_1.write(reinterpret_cast<char*>(&_dynamic_array_synapses_delay_1[0]), _dynamic_array_synapses_delay_1.size()*sizeof(_dynamic_array_synapses_delay_1[0]));
		    outfile__dynamic_array_synapses_delay_1.close();
		}
	} else
	{
		std::cout << "Error writing output file for _dynamic_array_synapses_delay_1." << endl;
	}
	ofstream outfile__dynamic_array_synapses_lastupdate;
	outfile__dynamic_array_synapses_lastupdate.open(results_dir + "_dynamic_array_synapses_lastupdate_3710850267", ios::binary | ios::out);
	if(outfile__dynamic_array_synapses_lastupdate.is_open())
	{
        if (! _dynamic_array_synapses_lastupdate.empty() )
        {
			outfile__dynamic_array_synapses_lastupdate.write(reinterpret_cast<char*>(&_dynamic_array_synapses_lastupdate[0]), _dynamic_array_synapses_lastupdate.size()*sizeof(_dynamic_array_synapses_lastupdate[0]));
		    outfile__dynamic_array_synapses_lastupdate.close();
		}
	} else
	{
		std::cout << "Error writing output file for _dynamic_array_synapses_lastupdate." << endl;
	}
	ofstream outfile__dynamic_array_synapses_N_incoming;
	outfile__dynamic_array_synapses_N_incoming.open(results_dir + "_dynamic_array_synapses_N_incoming_1151751685", ios::binary | ios::out);
	if(outfile__dynamic_array_synapses_N_incoming.is_open())
	{
        if (! _dynamic_array_synapses_N_incoming.empty() )
        {
			outfile__dynamic_array_synapses_N_incoming.write(reinterpret_cast<char*>(&_dynamic_array_synapses_N_incoming[0]), _dynamic_array_synapses_N_incoming.size()*sizeof(_dynamic_array_synapses_N_incoming[0]));
		    outfile__dynamic_array_synapses_N_incoming.close();
		}
	} else
	{
		std::cout << "Error writing output file for _dynamic_array_synapses_N_incoming." << endl;
	}
	ofstream outfile__dynamic_array_synapses_N_outgoing;
	outfile__dynamic_array_synapses_N_outgoing.open(results_dir + "_dynamic_array_synapses_N_outgoing_1673144031", ios::binary | ios::out);
	if(outfile__dynamic_array_synapses_N_outgoing.is_open())
	{
        if (! _dynamic_array_synapses_N_outgoing.empty() )
        {
			outfile__dynamic_array_synapses_N_outgoing.write(reinterpret_cast<char*>(&_dynamic_array_synapses_N_outgoing[0]), _dynamic_array_synapses_N_outgoing.size()*sizeof(_dynamic_array_synapses_N_outgoing[0]));
		    outfile__dynamic_array_synapses_N_outgoing.close();
		}
	} else
	{
		std::cout << "Error writing output file for _dynamic_array_synapses_N_outgoing." << endl;
	}
	ofstream outfile__dynamic_array_synapses_w;
	outfile__dynamic_array_synapses_w.open(results_dir + "_dynamic_array_synapses_w_441891901", ios::binary | ios::out);
	if(outfile__dynamic_array_synapses_w.is_open())
	{
        if (! _dynamic_array_synapses_w.empty() )
        {
			outfile__dynamic_array_synapses_w.write(reinterpret_cast<char*>(&_dynamic_array_synapses_w[0]), _dynamic_array_synapses_w.size()*sizeof(_dynamic_array_synapses_w[0]));
		    outfile__dynamic_array_synapses_w.close();
		}
	} else
	{
		std::cout << "Error writing output file for _dynamic_array_synapses_w." << endl;
	}

	ofstream outfile__dynamic_array_statemonitor_w;
	outfile__dynamic_array_statemonitor_w.open(results_dir + "_dynamic_array_statemonitor_w_1952857788", ios::binary | ios::out);
	if(outfile__dynamic_array_statemonitor_w.is_open())
	{
        for (int n=0; n<_dynamic_array_statemonitor_w.n; n++)
        {
            if (! _dynamic_array_statemonitor_w(n).empty())
            {
                outfile__dynamic_array_statemonitor_w.write(reinterpret_cast<char*>(&_dynamic_array_statemonitor_w(n, 0)), _dynamic_array_statemonitor_w.m*sizeof(_dynamic_array_statemonitor_w(0, 0)));
            }
        }
        outfile__dynamic_array_statemonitor_w.close();
	} else
	{
		std::cout << "Error writing output file for _dynamic_array_statemonitor_w." << endl;
	}
	// Write last run info to disk
	ofstream outfile_last_run_info;
	outfile_last_run_info.open(results_dir + "last_run_info.txt", ios::out);
	if(outfile_last_run_info.is_open())
	{
		outfile_last_run_info << (Network::_last_run_time) << " " << (Network::_last_run_completed_fraction) << std::endl;
		outfile_last_run_info.close();
	} else
	{
	    std::cout << "Error writing last run info to file." << std::endl;
	}
}

void _dealloc_arrays()
{
	using namespace brian;


	// static arrays
	if(_static_array__array_statemonitor__indices!=0)
	{
		delete [] _static_array__array_statemonitor__indices;
		_static_array__array_statemonitor__indices = 0;
	}
}

