clear all
close all
clc

%%


impDat = importdata(['../postProcessing/forces/0/forceCoeffs.dat'],'\t', 9);


time = impDat.data(:,1);

Cm = impDat.data(:,2);
Cd = impDat.data(:,3);
Cl = impDat.data(:,4);
Clf = impDat.data(:,5);
Clr = impDat.data(:,6);

%%


figure(1)
hold off
plot(time, Cm, 'b')
hold on
grid on
plot(time, Cd, 'r')
plot(time, Cl, 'm')
plot(time, Clf, 'c')
plot(time, Clr, 'k')


%% analytical frequency

uIn = 0.004012;
dCyl = 0.05;

Sr = 0.2;


fAna = Sr*uIn/dCyl;


%% determine frequency

N = round(length(time)/2);
%N = 1;

timeVec = time(N:end)-time(N);
dataVec = Cl(N:end);
dataVec = Cl(N:end)-mean(Cl(N:end));

zp = 4; % zero padding

Fs = 1/mean(diff(timeVec)); % thats where the dirt hides.
L = length(dataVec);
NFFT = zp*2^nextpow2(L);
Y = fft(dataVec,NFFT)/L;
f = Fs/2*linspace(0,1,NFFT/2+1);
S = abs(Y(1:NFFT/2+1));

[sm, ix] = max(S);

fNum = f(ix);


disp(["Karman vortex frequency : ",num2str(fAna)," Hz"])
disp(["numerically determined frequency : ",num2str(fNum)," Hz"])


figure(2)
hold off
plot(f, S, 'b')
grid on
hold on
plot(fAna*[1 1], max(S)*[0 1], 'k--')

xlim([0 4*fAna])




figure(3)
plot(timeVec, dataVec)




