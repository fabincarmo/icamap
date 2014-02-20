module parametros
    implicit none
    integer, parameter :: Nf = 64
end module parametros

subroutine func(beta,f_c)
implicit none
double precision, intent(in) :: beta
double precision, intent(inout) :: f_c
f_c=GAMMA(3.0d+0*(1.0d+0+beta)/2.0d+0)**(1.0d+0/(1.0d+0+beta))/GAMMA((1.0d+0+beta)/2.0d+0)**(1.0d+0/(1.0d+0+beta))
end subroutine func

subroutine derivfun(var,beta,arg,saida)
use parametros
implicit none
integer n
double precision, intent(in) :: var
double precision, intent(in), dimension(Nf) :: beta,arg
double precision, intent(inout), dimension(Nf) :: saida
double precision fc
do n = 1,Nf
 call func(beta(n),fc)
 saida(n) = (2.0d+0*fc/((1.0d+0+beta(n))*sqrt(var)))*((abs(arg(n))/sqrt(var)) &
            **((1.0d+0-beta(n))/(1.0d+0+beta(n))))
end do
do n = 1,Nf
 saida(n)=sign(saida(n),arg(n))
end do
end subroutine derivfun

subroutine alggrad(x,y,bx,bv,Wx,Wv,var,lamb,maxits,limg)
use parametros
implicit none
integer i,j,k,T
integer, intent(in) :: maxits
double precision, intent(inout), dimension(:) :: x
double precision, intent(in), dimension(:) :: y
double precision, intent(in), dimension(Nf) :: bx,bv
double precision, dimension(Nf) :: v,sv,sx,dx,dv,gr
double precision, intent(in), dimension(Nf,Nf) :: Wx,Wv
double precision, intent(in) :: var,limg,lamb
double precision lambi
T=size(x)-Nf+1
do k=1,T
write(*,"(a1,'Executando:'f8.1'%')",advance="no") achar(13),100.*real(k)/real(T)
do i=1,maxits
 v = y(k:k+Nf-1) - x(k:k+Nf-1)
 sv = matmul(Wv,v(Nf:1:-1))
 sx = matmul(Wx,x(k+Nf-1:k:-1))
 call derivfun(var,bv,sv,dv)
 call derivfun(1.0d+0,bx,sx,dx)
 gr=matmul(transpose(Wv),dv)-matmul(transpose(Wx),dx)
 do j=1,Nf
  if (abs(gr(j))>limg) gr(j)=sign(limg,gr(j))
 enddo
 lambi = (1.0d+0/maxval(abs(gr)))*lamb
 x(k:k+Nf-1)=x(k:k+Nf-1)+lambi*gr(Nf:1:-1)
enddo
enddo
end subroutine alggrad
