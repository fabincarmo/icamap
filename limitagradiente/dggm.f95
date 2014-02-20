subroutine func(beta,f_c)
implicit none
double precision, intent(in) :: beta
double precision, intent(inout) :: f_c
f_c=GAMMA(3.0d+0*(1.0d+0+beta)/2.0d+0)**(1.0d+0/(1.0d+0+beta))/GAMMA((1.0d+0+beta)/2.0d+0)**(1.0d+0/(1.0d+0+beta))
end subroutine func

subroutine derivfun(var,beta,arg,saida)
implicit none
integer n
double precision, intent(in) :: var
double precision, intent(in), dimension(64) :: beta,arg
double precision, intent(inout), dimension(64) :: saida
double precision fc
do n = 1,64
 call func(beta(n),fc)
 saida(n) = (2.0d+0*fc/((1.0d+0+beta(n))*sqrt(var)))*((abs(arg(n))/sqrt(var)) &
            **((1.0d+0-beta(n))/(1.0d+0+beta(n))))
end do
do n = 1,64
 saida(n)=sign(saida(n),arg(n))
end do
end subroutine derivfun

subroutine alggrad(x,y,bx,bv,Wx,Wv,var,lamb,maxits,limg)
implicit none
integer i,j,k,T
integer jan
parameter (jan=64)
integer, intent(in) :: maxits
double precision, intent(inout), dimension(:) :: x
double precision, intent(in), dimension(:) :: y
double precision, intent(in), dimension(64) :: bx,bv
double precision, dimension(64) :: v,sv,sx,dx,dv,gr
double precision, intent(in), dimension(64,64) :: Wx,Wv
double precision, intent(in) :: var,limg,lamb
double precision lambi
T=size(x)-63
do k=1,T
write(*,"(a1,'Executando:'f8.1'%')",advance="no") achar(13),100.*real(k)/real(T)
do i=1,maxits
 v = y(k:k+63) - x(k:k+63)
 sv = matmul(Wv,v(64:1:-1))
 sx = matmul(Wx,x(k+63:k:-1))
 call derivfun(var,bv,sv,dv)
 call derivfun(1.0d+0,bx,sx,dx)
 gr=matmul(transpose(Wv),dv)-matmul(transpose(Wx),dx)
 do j=1,64
  if (abs(gr(j))>limg) gr(j)=sign(limg,gr(j))
 enddo
 lambi = (1.0d+0/maxval(abs(gr)))*lamb
 x(k:k+63)=x(k:k+63)+lambi*gr(64:1:-1)
enddo
enddo
end subroutine alggrad
