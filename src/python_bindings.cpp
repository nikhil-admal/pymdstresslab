#include "pybind11/numpy.h"
#include "pybind11/pybind11.h"
#include "pybind11/eigen.h"
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
           .def(py::init<const MethodSphere &, Grid<Current>* >())
           .def("write", py::overload_cast<const std::string &>(&Stress<MethodSphere,Cauchy>::write))
           .def("write", py::overload_cast<>(&Stress<MethodSphere,Cauchy>::write));

   py::class_<Stress<MethodSphere,Piola> >(m, "StressPiola")
           .def(py::init<std::string, const MethodSphere &, Grid<Reference>* >())
           .def(py::init<const MethodSphere &, Grid<Reference>* >())
           .def("write", py::overload_cast<const std::string &>(&Stress<MethodSphere,Piola>::write))
           .def("write", py::overload_cast<>(&Stress<MethodSphere,Piola>::write));

    // calculates one Cauchy stress
    m.def("calculateStress",[](BoxConfiguration& body, Kim& kim, std::tuple<Stress<MethodSphere,Cauchy>&> cauchyStress){
        std::cout << "here\n";
       calculateStress(body, kim, std::tie(std::get<0>(cauchyStress)));
   });
   m.def("calculateStress",[](BoxConfiguration& body, Kim& kim, Stress<MethodSphere,Cauchy> cauchyStress){
        std::cout << "here\n";
       calculateStress(body, kim, std::tie(cauchyStress));
   });

   // calculates one Piola stress
   m.def("calculateStress",[](BoxConfiguration& body, Kim& kim, std::tuple<Stress<MethodSphere,Piola>&> piolaStress){
       calculateStress(body, kim, std::tie(std::get<0>(piolaStress)));
   });
   m.def("calculateStress",[](BoxConfiguration& body, Kim& kim, Stress<MethodSphere,Piola> piolaStress){
       calculateStress(body, kim, std::tie(piolaStress));
   });

   // calculates a couple of Cauchy stresses
   m.def("calculateStress",[](BoxConfiguration& body, Kim& kim, std::tuple<Stress<MethodSphere,Cauchy>&, Stress<MethodSphere,Cauchy>&> stress){
       calculateStress(body, kim, std::tie(std::get<0>(stress),std::get<1>(stress)));
   });

   // calculates a couple of Piola stresses
   m.def("calculateStress",[](BoxConfiguration& body, Kim& kim, std::tuple<Stress<MethodSphere,Piola>&, Stress<MethodSphere,Piola>&> stress){
       calculateStress(body, kim, std::tie(std::get<0>(stress),std::get<1>(stress)));
   });

   // calculates a couple of Piola stresses, and a couple of Cauchy stresses
   m.def("calculateStress",[](BoxConfiguration& body, Kim& kim,
                              std::tuple<Stress<MethodSphere,Piola>&,  Stress<MethodSphere,Piola>&>  piolaStress,
                              std::tuple<Stress<MethodSphere,Cauchy>&, Stress<MethodSphere,Cauchy>&> cauchyStress){
       calculateStress(body, kim, std::tie(std::get<0>(piolaStress),std::get<1>(piolaStress)),
                                  std::tie(std::get<0>(cauchyStress),std::get<1>(cauchyStress)));
   });
}
