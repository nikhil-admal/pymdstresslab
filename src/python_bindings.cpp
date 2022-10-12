#include "pybind11/numpy.h"
#include "pybind11/pybind11.h"
#include "pybind11/eigen.h"
#include "pybind11/operators.h"
#include "pybind11/functional.h"
#include "pybind11/stl.h"
#include "typedef.h"
#include <deque>
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
#include "MethodUser.h"
#include "Polynomial.h"
#include "MethodLdad.h"

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
            .def("read",&Grid<Current>::write)
            .def_readonly("coordinates",&Grid<Current>::coordinates);

    py::class_<Grid<Reference>,GridBase>(m, "GridReference")
            .def(py::init<int>())
            .def(py::init<Vector3d, Vector3d, int, int, int>())
            .def(py::init<std::string>())
            .def("read",&Grid<Reference>::read)
            .def("read",&Grid<Reference>::write)
            .def_readonly("coordinates", &Grid<Reference>::coordinates);
            
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
        calculateStress(body, kim, std::tie(std::get<0>(cauchyStress)));
    });
    m.def("calculateStress",[](BoxConfiguration& body, Kim& kim, Stress<MethodSphere,Cauchy> cauchyStress){
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

//    TRY1 Trampoline classes

    class PyMethodUser : public MethodUser{
    public:
    using MethodUser::MethodUser;
    double operator()(const Vector3d& vec) const override {PYBIND11_OVERRIDE_PURE_NAME(
        double,
        MethodUser,
        "__call__",
        operator(),
        vec
    );}
    double bondFunction(const Vector3d& vec1, const Vector3d& vec2) const override {PYBIND11_OVERRIDE_PURE(
        double,
        MethodUser,
        bondFunction,
        vec1, vec2
    );}
    };

    py::class_<MethodUser,PyMethodUser>(m, "MethodUser")
        .def(py::init<double>())
        .def("bondFunction", &MethodUser::bondFunction, "bind function")
        .def("__call__", &MethodUser::operator(), "call operator");

    py::class_<Polynomial>(m, "Polynomial")
        .def(py::init<>())
        .def(py::init<std::deque<double>&>())
        .def_readwrite("coefficients", &Polynomial::coefficients, "coefficients")
        .def("__call__",[](Polynomial &p, double& arg){p(arg);},"Operator ()");

    py::class_<Stress<MethodUser,Cauchy> >(m, "StressCauchyUser")
            .def(py::init<std::string,const MethodUser &, Grid<Current>* >())
            .def(py::init<const MethodUser &, Grid<Current>* >())
            .def("write", py::overload_cast<const std::string &>(&Stress<MethodUser,Cauchy>::write))
            .def("write", py::overload_cast<>(&Stress<MethodUser,Cauchy>::write));

    py::class_<Stress<MethodUser,Piola> >(m, "StressPiolaUser")
            .def(py::init<std::string, const MethodUser &, Grid<Reference>* >())
            .def(py::init<const MethodUser &, Grid<Reference>* >())
            .def("write", py::overload_cast<const std::string &>(&Stress<MethodUser,Piola>::write))
            .def("write", py::overload_cast<>(&Stress<MethodUser,Piola>::write));

    m.def("calculateStress",[](BoxConfiguration& body, Kim& kim, Stress<MethodUser,Cauchy> cauchyStress){
        calculateStress(body, kim, std::tie(cauchyStress));
    });

    m.def("calculateStress",[](BoxConfiguration& body, Kim& kim, Stress<MethodUser,Piola> piolaStress){
        calculateStress(body, kim, std::tie(piolaStress));
    });

    m.def("test_user_bond",[](const Vector3d& vec1, const Vector3d& vec2, MethodUser &mu){
        auto r = mu.bondFunction(vec1, vec2);
        return r;
    });

    m.def("test_user_op", [](const Vector3d& vec, MethodUser &mu){
        std::cout << mu.bondFunction(vec, vec) << "\n";
        auto r = mu( vec);
        return r;
    });

    py::class_<MethodLdadConstant>(m, "MethodLdadConstant")
            .def(py::init<const Matrix3d&>());
    py::class_<MethodLdadTrigonometric>(m, "MethodLdadTrigonometric")
            .def(py::init<const Matrix3d&>());


}
