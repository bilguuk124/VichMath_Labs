package main;

import java.util.ArrayList;

public class Matrix {
    public static int SIZE = -1;
    public static boolean isSwitched = false;

    public static double[][] matrixA;
    public static double[][] matrixB;
    public static double[][] matrixX1;
    public static double[][] matrixX2;

    public static double epsilon;
    public static int M;

    public static ArrayList<Double> maxes;

    public static void setMatrixAandB(double[][] mainMatrix){
        matrixA = new double[SIZE][SIZE];
        matrixB = new double[SIZE][1];
        maxes = new ArrayList<Double>(SIZE);

        for(int i = 0; i < SIZE; i++){
            for(int j = 0; j < SIZE; j++){
                matrixA[i][j] = mainMatrix[i][j];
            }
            matrixB[i][0] = mainMatrix[i][SIZE];
        }

        System.out.println("До перестановки: ");
        for(int i = 0; i < SIZE; i++){
            for (int j = 0; j < SIZE; j ++){
                System.out.print(matrixA[i][j] + "  ");
            }
            System.out.print(matrixB[i][0]);
            System.out.println();
        }
        setDiagonalDominance();
        System.out.println("После перестановки: ");
        for(int i = 0; i < SIZE; i++){
            for (int j = 0; j < SIZE; j ++){
                System.out.print(matrixA[i][j] + "  ");
            }
            System.out.print(matrixB[i][0]);
            System.out.println();
        }

        System.out.println("\nПосле извлечение матрицу C:");
        for (int i = 0; i < SIZE; i++){
            for (int j = 0; j < SIZE; j++){
                if(matrixA[i][j] / maxes.get(i) != 1D){
                    matrixA[i][j] /= -maxes.get(i);
                }
                else {
                    matrixA[i][j] = 0;
                }
            }
            matrixB[i][0] /= maxes.get(i);
        }
        for(int i = 0; i < SIZE; i++){
            for (int j = 0; j < SIZE; j ++){
                System.out.print(matrixA[i][j] + "  ");
            }
            System.out.print(matrixB[i][0]);
            System.out.println();
        }

    }

    public static void switchLines(int i, int j){
        double[] tmp = matrixA[i];
        matrixA[i] = matrixA[j];
        matrixA[j] = tmp;

        double[] tmpB = matrixB[i];
        matrixB[i] = matrixB[j];
        matrixB[j] = tmpB;
    }

    public static int shufflingRows(int numberX){
        int currentX = numberX;
        double currentCoef;
        double sumOfOther;

        for(int i = numberX; i < SIZE; i++){
            sumOfOther = 0;
            currentCoef = Math.abs(matrixA[i][currentX]);
            for(int j = 0; j < SIZE; j ++){
                sumOfOther += Math.abs(matrixA[i][j]);
            }
            sumOfOther -= currentCoef;
            if (currentCoef >= sumOfOther){
                if (currentCoef > sumOfOther){
                    isSwitched = true;
                    maxes.add(currentCoef);
                }
                switchLines(numberX, i);
                return i;
            }
        }
        System.err.println("Не получается переставить строчки так чтобы выполнилось диагональное преобладание");
        System.exit(4);
        return -1;
    }

    public static void setDiagonalDominance(){
        for(int i = 0; i < SIZE; i++){
            shufflingRows(i);
        }
        if(isSwitched){
            System.out.println('\n');
        }
        else{
            System.err.println("Не выполнено условие о том чтобы при заменах сходились итерации");
            System.exit(5);
        }
    }

    public static void initMatrixX1andX2(){
        matrixX2 = new double[SIZE][1];
        matrixX1 = new double[SIZE][1];
        for (int i = 0; i < SIZE; i++){
            matrixX2[i][0] = matrixB[i][0];
        }
    }

    public static void iteration(){
        for (int i = 0; i < SIZE; i++){
            matrixX1[i][0] = matrixX2[i][0];
        }
        for (int i = 0 ; i < SIZE; i++){
            double sumOfOther = 0;
            for (int j = 0; j < SIZE; j++){
                if(j!=i){
                    sumOfOther += matrixA[i][j]*matrixX1[j][0];
                }
            }
            sumOfOther += matrixB[i][0];
            matrixX2 [i][0] = sumOfOther;
        }
    }
    public static boolean checkAllNewX(){
        for(int i = 0; i < SIZE; i++){
            if(Math.abs(matrixX2[i][0] - matrixX1[i][0]) > epsilon){
                return false;
            }
        }
        return true;
    }

    public static void start(){
        int count = 0;

        do {
            iteration();
            count++;
        } while (!checkAllNewX() && count < M);

        System.out.println("\nПосле работы программы");
        for(int i = 0; i < SIZE; i++){
            System.out.println("X" + (i+1) + " = " + matrixX2[i][0]);
        }

        if (count>=M){
            System.out.println("\nИтерации не сходятся(на заданном максимальном их количестве)");
        }
        else{
            System.out.println("\nОбщее количество итерации = " + count + "\n");
        }

        for( int i = 0; i < SIZE; i ++){
            System.out.println("Вектор погрешности вектора X_" + (i+1) + " = " + Math.abs(matrixX2[i][0] - matrixX1[i][0]));
        }
    }

}