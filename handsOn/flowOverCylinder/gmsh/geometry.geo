



// main dimensions
D = 0.05;
L = 2.5;
W = 1.0;
C = 0.4;

R = D/2;

dx = 0.035;
dr = 0.015;


H = 0.01;


// outer domain
Point(1) = {0, -W/2, 0, dx};
Point(2) = {L, -W/2, 0, dx};
Point(3) = {L,  W/2, 0, dx};
Point(4) = {0,  W/2, 0, dx};

Line(1)  = {1 , 2};
Line(2)  = {2 , 3};
Line(3)  = {3 , 4};
Line(4)  = {4 , 1};

Line Loop(1) = {1,2,3,4};

// cylinder center
Point(5) = {C, 0, 0, dr};

Point(6) = {C+R, 0, 0, dr};
Point(7) = {C, R, 0, dr};
Point(8) = {C-R, 0, 0, dr};
Point(9) = {C, -R, 0, dr};

Circle(5) = {6,5,7};
Circle(6) = {7,5,8};
Circle(7) = {8,5,9};
Circle(8) = {9,5,6};

Line Loop(2) = {5,6,7,8};


Plane Surface(1) = {1,2};

Recombine Surface {1};

surfaceVector[] =Extrude {0, 0, H} {
    Surface{1};
    Layers{1};
    Recombine;
};


/* surfaceVector contains in the following order:
[0]	- front surface (opposed to source surface)
[1] - extruded volume
[2] - bottom surface (belonging to 1st line in "Line Loop (6)")
[3] - right surface (belonging to 2nd line in "Line Loop (6)")
[4] - top surface (belonging to 3rd line in "Line Loop (6)")
[5] - left surface (belonging to 4th line in "Line Loop (6)") */
Physical Surface("front") = surfaceVector[0];
Physical Volume("internal") = surfaceVector[1];
Physical Surface("sideBottom") = surfaceVector[2];
Physical Surface("outlet") = surfaceVector[3];
Physical Surface("sideTop") = surfaceVector[4];
Physical Surface("inlet") = surfaceVector[5];
Physical Surface("back") = {1}; // from Plane Surface (1) ...


