#include "pybind11/numpy.h"
#include "pybind11/pybind11.h"
#include "pybind11/eigen.h"
#include "typedef.h"
#include <map>

#include <string>

#include "BoxConfiguration.h"
#include "kim.h"
#include "Grid.h"
#include "MethodSphere.h"
#include "Stress.h"
#include "calculateStress.h"
#include "SubConfiguration.h"
#include "Stencil.h"

namespace py = pybind11;

PYBIND11_MODULE(pymdstresslab, m){
    py::class_<Configuration>(m,"Configuration")
            .def(py::init<int,int>());

    py::class_<BoxConfiguration, Configuration>(m, "BoxConfiguration")
            .def(py::init<int,int>())
            //  .def(py::init<std::string, int>())
            .def("read",&BoxConfiguration::read)
            .def("getConfiguration",&BoxConfiguration::getConfiguration);

    py::class_<Kim>(m, "Kim")
            .def(py::init<>())
            .def(py::init<std::string>());

    py::class_<GridBase>(m, "GridBase")
            .def(py::init<>());

    py::class_<Grid<Current>,GridBase>(m, "GridCurrent")
            .def(py::init<int>())
            .def(py::init<Vector3d, Vector3d, int, int, int>())
            .def(py::init<std::string>())
            .def("read",&Grid<Current>::read)
            .def("read",&Grid<Current>::write);

    py::class_<Grid<Reference>,GridBase>(m, "GridReference")
            .def(py::init<int>())
            .def(py::init<Vector3d, Vector3d, int, int, int>())
            .def(py::init<std::string>())
            .def("read",&Grid<Reference>::read)
            .def("read",&Grid<Reference>::write);
            
    py::class_<MethodSphere>(m, "MethodSphere")
            .def(py::init<double, std::string>())
            .def(py::init<double, std::map<double,double> >())
            .def(py::init<const MethodSphere&>());
        
   py::class_<Stress<MethodSphere,Cauchy> >(m, "StressCauchy")
           .def(py::init<std::string,const MethodSphere &, Grid<Current>* >())
           .def(py::init<const MethodSphere &, Grid<Current>* >());
   py::class_<Stress<MethodSphere,Piola> >(m, "StressPiola")
           .def(py::init<std::string, const MethodSphere &, Grid<Reference>* >())
           .def(py::init<const MethodSphere &, Grid<Reference>* >());

//    py::class_<Stencil>(m, "Stencil")
//            .def(py::init<Configuration&>());
//    py::class_<SubConfiguration,Configuration>(m, "SubConfiguration")
//            .def(py::init<Stencil &>());
//    py::class_<InteratomicForces>(m, "InteratomicForces")
//            .def(py::init<NeighList*>());

    // calculates one Cauchy stress
//    m.def("calculateStress",[](BoxConfiguration& body, Kim& kim, std::tuple<Stress<Sphere,Cauchy>&> cauchyStress){
//        calculateStress(body, kim, std::tie(std::get<0>(cauchyStress)));
//    });
//
//    // calculates one Piola stress
//    m.def("calculateStress",[](BoxConfiguration& body, Kim& kim, std::tuple<Stress<Sphere,Piola>&> piolaStress){
//        calculateStress(body, kim, std::tie(std::get<0>(piolaStress)));
//    });
//
//    // calculates a couple of Cauchy stresses
//    m.def("calculateStress",[](BoxConfiguration& body, Kim& kim, std::tuple<Stress<Sphere,Cauchy>&, Stress<Sphere,Cauchy>&> stress){
//        calculateStress(body, kim, std::tie(std::get<0>(stress),std::get<1>(stress)));
//    });
//
//    // calculates a couple of Piola stresses
//    m.def("calculateStress",[](BoxConfiguration& body, Kim& kim, std::tuple<Stress<Sphere,Piola>&, Stress<Sphere,Piola>&> stress){
//        calculateStress(body, kim, std::tie(std::get<0>(stress),std::get<1>(stress)));
//    });
//
//    // calculates a couple of Piola stresses, and a couple of Cauchy stresses
//    m.def("calculateStress",[](BoxConfiguration& body, Kim& kim,
//                               std::tuple<Stress<Sphere,Piola>&,  Stress<Sphere,Piola>&>  piolaStress,
//                               std::tuple<Stress<Sphere,Cauchy>&, Stress<Sphere,Cauchy>&> cauchyStress){
//        calculateStress(body, kim, std::tie(std::get<0>(piolaStress),std::get<1>(piolaStress)),
//                                   std::tie(std::get<0>(cauchyStress),std::get<1>(cauchyStress)));
//    });
}
