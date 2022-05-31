package main;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Scanner;

public class Main {

    private static Scanner getInfo() throws FileNotFoundException{
        Scanner scanner = new Scanner(System.in);
        System.out.println("Ввести с файла(+) или с консоли(-)?");
        String str = scanner.nextLine();
        boolean isFile = false;
        while(true){
            if(str.equalsIgnoreCase("+")){
                isFile = true;
                break;
            }
            if(str.equalsIgnoreCase("-")){
                break;
            }
            System.out.println("Нужно ввести либо + либо -");
            str = scanner.nextLine();
        }

        if (isFile){
            File file = new File("input.txt");
            scanner = new Scanner(file);
        } else{
            System.out.println("Введите размер матрицы, точность решения и максимум количество итерации");
        }
        return scanner;
    }

    public static void main(String[] args) {
        Scanner scanner;
        try{
            scanner = getInfo();
        } catch (FileNotFoundException e){
            System.out.println("Файл не найден! Введем с консоли");
            scanner = new Scanner(System.in);
        }

        int n = scanner.nextInt();

        Matrix.epsilon = scanner.nextDouble();

        Matrix.M = scanner.nextInt();

        System.out.println("Введем матрицу строк за строкой");
        double[][] startMatrix = new double[n][n+1];
        for (int i = 0; i < n; ++i){
            for (int j = 0; j < n + 1; ++j){
                startMatrix[i][j] = scanner.nextDouble();
            }
        }
        Matrix.SIZE = n;
        Matrix.setMatrixAandB(startMatrix);
        Matrix.initMatrixX1andX2();
        Matrix.start();

    }
}
