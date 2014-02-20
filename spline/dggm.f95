module parametros
    implicit none
    integer, parameter :: Nf = 64
end module parametros

subroutine func(beta,f_c)
implicit none
double precision, intent(in) :: beta
double precision, intent(inout) :: f_c
f_c = GAMMA(3.0d+0*(1.0d+0+beta)/2.0d+0)**(1.0d+0/(1.0d+0+beta))
f_c = f_c / GAMMA((1.0d+0+beta)/2.0d+0)**(1.0d+0/(1.0d+0+beta))
end subroutine func

subroutine derivfun(var,beta,arg,lim,params,saida)
use parametros
implicit none
integer i
double precision, intent(in) :: var
double precision, intent(in), dimension(Nf,4) :: params
double precision, intent(in), dimension(Nf) :: beta,lim
double precision, intent(inout), dimension(Nf) :: saida,arg
double precision fc,h00,h10,h01,h11
do i = 1,Nf,1
 call func(beta(i),fc)
 saida(i) = (2.0d+0*fc/((1.0d+0+beta(i))*sqrt(var)))*((abs(arg(i))/sqrt(var)) &
            **((1.0d+0-beta(i))/(1.0d+0+beta(i))))
end do
do i = 1,Nf,1
 if (abs(arg(i))<lim(i)) then
  arg(i)=(arg(i)+lim(i))/(2.0d+0*lim(i))
  h00=2.0d+0*arg(i)**3.0d+0-3.0d+0*arg(i)**2.0d+0+1.0d+0
  h10=arg(i)**3.0d+0-2.0d+0*arg(i)**2.0d+0+arg(i)
  h01=-2.0d+0*arg(i)**3.0d+0+3.0d+0*arg(i)**2.0d+0
  h11=arg(i)**3.0d+0-arg(i)**2.0d+0
  saida(i)=h00*params(i,1)+h10*2*lim(i)*params(i,2)+ &
           h01*params(i,3)+h11*2*lim(i)*params(i,4)
 else
  saida(i)=sign(saida(i),arg(i))
 endif
end do
end subroutine derivfun

subroutine alggrad(x,y,bx,bv,Wx,Wv,var,lamb,maxits,limx,limv,paramsx,paramsv)
use parametros
implicit none
integer i,k,T
integer, intent(in) :: maxits
double precision, intent(inout), dimension(:) :: x
double precision, intent(in), dimension(:) :: y
double precision, intent(in), dimension(Nf) :: bx,bv,limx,limv
double precision, dimension(Nf) :: v,sv,sx,dx,dv,gr
double precision, intent(in), dimension(Nf,Nf) :: Wx,Wv
double precision, intent(in) :: var
double precision, intent(in) :: lamb
double precision :: lambi
double precision, dimension(Nf,4) :: paramsx,paramsv
T=size(x)-Nf+1
do k=1,T,1
write(*,"(a1,'Executando:'f8.1'%')",advance="no") achar(13),100.*real(k)/real(T)
do i=1,maxits,1
 v = y(k:k+Nf-1)-x(k:k+Nf-1)
 sv = matmul(Wv,v(Nf:1:-1))
 sx = matmul(Wx,x(k+Nf-1:k:-1))
 call derivfun(var,bv,sv,limv,paramsv,dv)
 call derivfun(1.0d+0,bx,sx,limx,paramsx,dx)
 gr=matmul(transpose(Wv),dv)-matmul(transpose(Wx),dx)
 lambi = (lamb/maxval(abs(gr)))
 x(k:k+Nf-1)=x(k:k+Nf-1)+lambi*gr(Nf:1:-1)
enddo
enddo
end subroutine alggrad

